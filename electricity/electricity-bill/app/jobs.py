# -*- coding: utf-8 -*-
import configparser
from _datetime import datetime
import threading
import time

import cx_Oracle
import math

from flask import current_app

from app.models.arrears_data import ArrearsData
from app.models.current_qf import Current_Qf
from app.models.arrears_data import db
import psutil
import schedule
from sqlalchemy.sql import func
import os
from app.apis.v1 import get_branch_office
from app.apis.v1 import first_sync

from app.tools import send_service_mail

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
cf = configparser.ConfigParser()


def sync_increment(app):
    """
    增量同步数据库
    """
    """
    TODO 每天2:00AM同步数据库，查询源数据库中SSSJ>=数据库中最大SSSJ的记录
    数据库中最大的SSSJ即上次增量同步的最大SSSJ
    """
    with app.app_context():
        day = datetime.now().day
        if cf.getboolean('sync', 'FIRST_SYNC') and day in app.config['INCREMENTAL_SYNC_DATES']:
            max_sssj = db.session.query(
                func.max(ArrearsData.sssj)).all()[0][0]  # mysql的qfshuju表中最大的sssj，我们需要更新的部分就是oracle中sssj大于该SSSJ的数据
            if max_sssj is None:
                app.logger.info('因未完成首次同步，增量同步变首次同步')
                first_sync(app=current_app._get_current_object())
            else:
                my_db = cx_Oracle.connect(app.config['ORACLE_DATABASE_URI'])
                cr = my_db.cursor()
                sql = 'SELECT COUNT(*) ' \
                      ' FROM sjcq.npmis_ZW_SSDFJL' \
                      " WHERE TO_CHAR(SSSJ, 'yyyymmdd') > TO_CHAR(WYJRQ, 'yyyymmdd') AND YSDF > 0 AND " \
                      " TO_CHAR(SSSJ,'yyyymmdd') > TO_CHAR(TO_DATE('" + str(max_sssj) + "','yyyy-mm-dd hh24:mi:ss'),'yyyymmdd')"
                print("here")
                cr.execute(sql)
                rs1 = cr.fetchall()
                count = rs1[0][0]  # oracle满足条件的行数
                if count <= 0:
                    return
                available_memory = get_available_memory()  # 服务器可用内存大小
                batch_size = int(available_memory * 50000)  # 每次处理行数
                batch_size = max(batch_size, 500000)
                n = int(math.ceil(float(count) / batch_size))

                for i in range(n):
                    sql = 'SELECT * FROM (SELECT A.*, ROWNUM RN FROM (SELECT DISTINCT YHBH,YHMC,YDDZ,DFNY,QF,YSWYJ,' \
                          'FLOOR(SSSJ - WYJRQ) QFSC, WYJRQ, SSSJ FROM sjcq.npmis_ZW_SSDFJL ' \
                          ' WHERE TO_CHAR(SSSJ, \'yyyymmdd\') > TO_CHAR(WYJRQ, \'yyyymmdd\') AND YSDF > 0 AND ' \
                          'SSSJ > to_date(\'' + str(max_sssj) + '\',\'yyyy-mm-dd hh24:mi:ss\')) A' \
                                                                ' WHERE ROWNUM <= ' + str(
                        (i + 1) * batch_size) + ') WHERE RN > ' + str(i * batch_size)

                    cr.execute(sql)
                    rs = cr.fetchall()
                    data = [{'YHBH': d[0], 'YHMC': d[1], 'YDDZ': d[2], 'DFNY': d[3],
                             'QF': d[4], 'YSWYJ': d[5], 'QFSC': d[6], 'WYJRQ': d[7], 'SSSJ': d[8]} for d in rs]
                    count_done = (i + 1) * batch_size if (i < n - 1) else count
                    insert_into_mysql_qfshuju(app, data, count_done)
                cr.close()
                my_db.close()
                app.logger.info('call stored procedure')
                call_stored_procedure(app)  # 调用mysql中的存储过程
                app.logger.info('此次增量同步完成')
                # 发送邮件通知
                send_service_mail('Incremental synchronization finish notification', app.config['ADMINS'],
                                  'Incremental synchronization finished at {}, {} rows was synchronized'.format(
                                      datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), count),
                                  app=app)
        else:
            app.logger.info('skip incremental sync')


def update_table():
    """
    计算违约风险
    """
    pass


def run_schedule(app):
    """
    Invoke schedule.
    """
    # For schedule rules please refer to https://github.com/dbader/schedule
    # schedule.every(20).minutes.do(update_view_times, app)
    # schedule.every(1).minute.do(test_insert)
    schedule.every().day.at(app.config['INCREMENTAL_SYNC_TIME']).do(sync_increment, app)
    schedule.every().day.at(app.config['CURRENT_QF_SYNC_TIME']).do(set_current_qf, app)
    while True:
        schedule.run_pending()
        time.sleep(1)


def init_schedule(app):
    """
    Init.
    """
    path = app.config['SNYC_CONFIG_PATH']
    cf.read(path)
    # http://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode/
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        t = threading.Thread(target=run_schedule, args=(app,))
        # Python threads don't die when the main thread exits, unless they are daemon threads.
        t.setDaemon(True)
        t.start()


def insert_into_mysql_qfshuju(app, data, count_done):
    """
    将欠费数据插入mysql数据库中
    """
    for d in data:
        branch_office = get_branch_office(str(d['YDDZ']))
        db.session.add(
            ArrearsData(yhbh=d['YHBH'], yhmc=d['YHMC'], yddz=d['YDDZ'], dfny=d['DFNY'], qf=d['QF'], yswyj=d['YSWYJ'],
                        sssj=d['SSSJ'], qfsc=d['QFSC'], wyjrq=d['WYJRQ'], fengxianzhi=None, branch_office=branch_office))
    db.session.commit()
    app.logger.debug('成功插入' + str(count_done) + '行；')


def get_available_memory():
    """
    获取当前服务器可用内存大小，单位为GB
    """
    pc_men = psutil.virtual_memory()
    div_gb_factor = (1024.0 ** 3)
    return float(pc_men.available / div_gb_factor)


def call_stored_procedure(app):
    """
    调用存储过程，在mysql中建立几个关键表并插入数据
    """
    db.session.execute('call getQFZhiBiao_step1')
    db.session.execute('call getQFZhiBiao_step2')  # 获取欠费指标表，分两步完成
    app.logger.debug('成功完成qfzhibiao表的创建')
    db.session.execute('call getQFFengXian')  # 获取每个用户的历史风险数据
    app.logger.debug('成功完成qffengxian表的创建')
    db.session.execute('call add_fengxiangzhi_to_qfshuju')
    app.logger.debug('成功将fengxian值插入qfshuju表中')
    db.session.execute('call save_qfzhibiao')
    app.logger.debug('将历史qfzhibiao存入qfzhibiao_history表中')


def set_current_qf(app):
    """
    从oracle中读取当月欠费用户，插入mysql当中.
    """
    with app.app_context():
        my_db = cx_Oracle.connect(app.config['ORACLE_DATABASE_URI'])
        cr = my_db.cursor()
        # 找出当月欠费用户的编号
        sql = "select  YHBH,YHMC,YDDZ,DFNY,QF,YSWYJ,WYJRQ from sjcq.npmis_ZW_QFJL"
        cr.execute(sql)
        rs = cr.fetchall()
        db.session.execute('TRUNCATE current_qf_tmp')  # current_qf只存储最新数据
        if rs:
            for d in rs:
                branch_office = get_branch_office(str(d[2]))
                db.session.add(
                    Current_Qf(yhbh=d[0], yhmc=d[1], yddz=d[2], dfny=d[3], qf=d[4],
                                yswyj=d[5], fengxianzhi=None, wyjrq=d[6], branch_office=branch_office)
                )
            db.session.commit()
            app.logger.debug('当月欠费用户更新完成')
        db.session.execute('call set_current_qf_fengxianzhi')
        cr.close()
        my_db.close()
