# -*- coding: utf-8 -*-
import configparser
import math
import os
from datetime import datetime
import datetime as dt

import cx_Oracle
import psutil
from flask import Blueprint, jsonify, request, current_app
from flask_restplus import Resource, Api
from sqlalchemy import and_
from sqlalchemy.sql import func

from app.extensions import excel
from app.models.arrears_data import ArrearsData
from app.models.current_qf import Current_Qf
from app.models.arrears_data import db
from app.tools import send_service_mail
from app.tools.decorator import async

v1 = Blueprint('v1', __name__)
api = Api(v1, version='1.0', title='Api', doc='/')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


@api.route('/arrears')
class ArrearsEndPoint(Resource):
    @api.param('threshold', 'threshold of risk')
    @api.param('month', 'max month')
    @api.param('history', 'query for historical records or not')
    @api.param('branch_office', 'branch office')
    @api.param('start', 'start')
    @api.param('length', 'number of records')
    def get(self):
        threshold = request.args.get('threshold', '0.8')
        month = request.args.get('month')
        start = request.args.get('start', None)
        length = request.args.get('length', None)
        draw = request.args.get('draw', None)
        history = request.args.get('history', 'false')  # 是否查询历史记录
        branch_office = request.args.get('branch_office', None)
        return get_arrears(threshold, month, branch_office, draw, start, length, history)


def get_arrears(threshold, month, branch_office, draw=None, start=None, length=None, history='false'):
    branch_office_cond = " AND branch_office='%s'" % branch_office
    month_cond = " AND dfny<='%s'" % month
    tab_name = 'current_qf' if history == 'false' else 'qfshuju'
    if start is None or length is None:
        sql = 'SELECT yhbh, yhmc, yddz, dfny, qf, yswyj, sssj, wyjrq FROM %s' \
              ' WHERE fengxianzhi >=' + threshold
        if branch_office != '全部':
            sql += branch_office_cond
        sql = sql % tab_name
        if history == 'false':
            sql += month_cond
    else:
        sql = 'SELECT COUNT(*) FROM %s' % tab_name
        result = db.session.execute(sql).fetchall()
        records_total = result[0][0]
        sql1 = ('SELECT COUNT(*) FROM %s WHERE fengxianzhi >=' + threshold) % tab_name
        sql2 = ('SELECT id FROM %s WHERE fengxianzhi >=' + threshold) % tab_name
        if branch_office != '全部':
            sql1 += branch_office_cond
            sql2 += branch_office_cond
        if history != 'false':
            sql1 += month_cond
            sql2 += month_cond
        result = db.session.execute(sql1).fetchall()
        records_filtered = result[0][0]
        sql2 += ' ORDER BY id LIMIT %s,1' % start
        result = db.session.execute(sql2).fetchall()

        # 以下是根据上面查到的ID去限制范围
        start_id = str(result[0][0]) if result else '1'
        sql = (
                          'SELECT yhbh, yhmc, yddz, dfny, qf, yswyj, sssj, wyjrq FROM %s WHERE fengxianzhi >=' + threshold) % tab_name
        if branch_office != '全部':
            sql += branch_office_cond
        if history != 'false':
            sql += month_cond
        sql += ' AND id>=%s LIMIT %s' % (start_id, length)
    result = db.session.execute(sql)
    data = [{'user_no': r.yhbh,
             'user_name': r.yhmc,
             'address': r.yddz,
             'fee_year_month': r.dfny,
             'arrears': r.qf,
             'liquidated_damages': r.yswyj,
             'time': datetime.strftime(r.sssj, '%Y%m%d') if r.sssj is not None else (
                 datetime.strftime(r.wyjrq, '%Y%m%d') if r.wyjrq is not None else '')} for r in
            result] if result else []
    list.sort(data, key=lambda x: x['user_no'])
    return jsonify(data=data, draw=draw, recordsTotal=records_total,
                   recordsFiltered=records_filtered) if start is not None else data


@api.route('/personalArrears')
class UserArrearsEndPoint(Resource):
    @api.param('month', 'max month')
    @api.param('user_name', 'user name')
    @api.param('user_no', 'userNo')
    def get(self):
        month = request.args.get('month')
        user_name = request.args.get('user_name')
        user_no = request.args.get('user_no')
        if user_name is None or user_name == '':
            result = ArrearsData.query.filter(and_(ArrearsData.yhbh == user_no, ArrearsData.dfny <= month)).all()
        else:
            result = ArrearsData.query.filter(
                and_(ArrearsData.yhbh == user_no, ArrearsData.dfny <= month, ArrearsData.yhmc == user_name)).all()
        data = [{'user_no': r.yhbh,
                 'user_name': r.yhmc,
                 'address': r.yddz,
                 'fee_year_month': r.dfny,
                 'arrears': r.qf,
                 'liquidated_damages': r.yswyj,
                 'time': datetime.strftime(r.sssj, '%Y%m%d')} for r in result]
        return jsonify(data=data)


@api.route('/risk/<string:user_no>')
class UserRiskEndPoint(Resource):
    @api.param('month', 'max month')
    @api.param('user_name', 'user name')
    def get(self, user_no):
        month = request.args.get('month')
        user_name = request.args.get('user_name')
        one_year_ago = datetime.strftime(datetime.strptime(month, '%Y%m') + dt.timedelta(days=-365), '%Y%m')
        sql = 'SELECT * FROM qfshuju WHERE yhbh="' + user_no + '" AND dfny <= ' + month + ' AND dfny >="' + one_year_ago + '"'
        if user_name is not None and user_name != '':
            # sql = 'SELECT * FROM qffengxian x, qfshuju y WHERE x.yhbh = y.yhbh AND x.bill_month = y.dfny' \
            #       ' AND x.yhbh="' + user_no + '" AND bill_month <= ' + month + ' AND y.yhmc = "' + user_name + '"'
            sql = 'SELECT * FROM qfshuju WHERE yhbh="' + user_no + '" AND dfny <= ' + month + ' AND dfny >="' + \
                  one_year_ago + '" AND yhmc = "' + user_name + '"'
        result = db.session.execute(sql).fetchall()
        # result = Risk.query.filter(and_(Risk.yhbh == user_no, Risk.bill_month <= month)).all()
        data = [{'risk': round(r.fengxianzhi, 3),
                 'month': r.DFNY} for r in result]
        return jsonify(data=data)


@api.route('/check_user_name')
class UserRiskEndPoint(Resource):
    @api.param('user_name', 'user name')
    def get(self):
        user_name = request.args.get('user_name')
        result = db.session.execute('SELECT YHBH,YHMC,YDDZ FROM qfshuju WHERE YHMC="' + user_name +
                                    ' "group by YHBH,YHMC').fetchall()
        # result = Risk.query.filter(and_(Risk.yhbh == user_no, Risk.bill_month <= month)).all()
        data = [{'yhbh': r.YHBH,
                 'yhmc': r.YHMC,
                 'yddz': r.YDDZ} for r in result]
        return jsonify(data=data)


@api.route('/sync_first_time')
class SyncFirstTime(Resource):
    def get(self):
        current_app.logger.debug('第一次数据同步开始')
        first_sync(app=current_app._get_current_object())
        return jsonify(success=True)


@api.route('/test')
class Test(Resource):
    """
       增量同步数据库
       """
    """
    TODO 每天2:00AM同步数据库，查询源数据库中SSSJ>=数据库中最大SSSJ的记录
    数据库中最大的SSSJ即上次增量同步的最大SSSJ
    """

    def get(self):
        app = current_app
        day = datetime.now().day
        cf = configparser.ConfigParser()
        path = app.config['SNYC_CONFIG_PATH']
        cf.read(path)
        if cf.getboolean('sync', 'FIRST_SYNC') and day in app.config['INCREMENTAL_SYNC_DATES']:
            max_sssj = db.session.query(
                func.max(ArrearsData.sssj)).all()[0][0]  # mysql的qfshuju表中最大的sssj，我们需要更新的部分就是oracle中sssj大于该SSSJ的数据
            my_db = cx_Oracle.connect(app.config['ORACLE_DATABASE_URI'])
            cr = my_db.cursor()
            sql = 'SELECT COUNT(*) ' \
                  ' FROM sjcq.npmis_ZW_SSDFJL' \
                  " WHERE TO_CHAR(SSSJ, 'yyyymmdd') > TO_CHAR(WYJRQ, 'yyyymmdd') AND YSDF > 0 AND " \
                  " TO_CHAR(SSSJ,'yyyymmdd') > TO_CHAR(TO_DATE('" + str(
                max_sssj) + "','yyyy-mm-dd hh24:mi:ss'),'yyyymmdd')"
            cr.execute(sql)
            rs1 = cr.fetchall()
            count = rs1[0][0]  # oracle满足条件的行数
            if count <= 0:
                return
            available_memory = get_available_memory()  # 服务器可用内存大小
            batch_size = 100  # 每次处理行数
            if available_memory < 1:
                batch_size = 10000
            elif 1 <= available_memory < 2:
                batch_size = 50000
            elif 2 <= available_memory < 3:
                batch_size = 200000
            elif 3 <= available_memory < 4:
                batch_size = 300000
            elif 4 <= available_memory < 5:
                batch_size = 400000
            elif 5 <= available_memory < 7:
                batch_size = 600000
            elif 7 <= available_memory:
                batch_size = 1000000
            n = int(math.ceil(float(count) / batch_size))
            # 每次处理十万行数据，n表示处理次数

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


@api.route('/test1')
class Test1(Resource):
    def get(self):
        set_current_qf(current_app)


# def set_qfshuju_is_current_qf(app):
#     """
#     从oracle中读取当月欠费用户，并在mysql中的qfshuju表中对应用户行的is_current_qf置1.
#     """
#     sql = 'update qfshuju set is_current_qf = 0 where is_current_qf = 1'
#     db.session.execute(sql)  # 先将qfshuju表所有的is_current_qf置0
#     my_db = cx_Oracle.connect(app.config['ORACLE_DATABASE_URI'])
#     cr = my_db.cursor()
#     # TODO 从当月欠费表中同步记录，如果在qfshuju中不存在则插入，否则什么也不做
#     # 找出当月欠费用户的编号
#     sql = "SELECT YHBH FROM SJCQ.NPMIS_ZW_QFJL WHERE dfny=(SELECT TO_CHAR(SYSDATE, 'yyyymm') FROM DUAL)"
#     cr.execute(sql)
#     rs = cr.fetchall()
#     if rs:
#         yhbh_qf = [x[0] for x in rs]
#         length = len(yhbh_qf)
#         batch_size = 10000
#         for i in range(int(math.ceil(length / batch_size))):
#             s_temp = '('
#             s_temp += ','.join(yhbh_qf[i * batch_size: (i + 1) * batch_size])
#             s_temp += ')'
#             # 将qfshuju表中对应的is_current_qf置1
#             sql = 'update qfshuju set is_current_qf = 1 where yhbh in ' + s_temp
#             db.session.execute(sql)
#         app.logger.debug('is_current_qf更新完成')
#     cr.close()
#     my_db.close()


def set_current_qf(app):
    """
    从oracle中读取当月欠费用户，插入mysql中.
    """
    with app.app_context():
        my_db = cx_Oracle.connect(app.config['ORACLE_DATABASE_URI'])
        cr = my_db.cursor()
        # 找出当月欠费用户的编号
        sql = "select  YHBH,YHMC,YDDZ,DFNY,QF,YSWYJ,WYJRQ from sjcq.npmis_ZW_QFJL"
        cr.execute(sql)
        rs = cr.fetchall()
        db.session.execute('TRUNCATE current_qf_tmp')  # current_qf_tmp只存储最新数据
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


def make_excel_list(data, fields):
    list_data = []
    # field = [x['field'] for x in fields]

    list_data.append(fields)
    for d in data:
        tmp = []
        for key, value in d.items():
            tmp.append(value)
        list_data.append(tmp)
    return list_data


@api.route('/export')
class ExportExcel(Resource):
    @api.param('threshold', 'threshold of risk')
    @api.param('month', 'max month')
    @api.param('file_name', 'name of file')
    def get(self):
        file_name = request.args.get('file_name', 'export')
        threshold = request.args.get('threshold', None)
        month = request.args.get('month', None)
        branch_office = request.args.get('branch_office', None)
        history = request.args.get('history')
        fields = ['用户编号', '用户名称', '用电地址', '电费年月', '欠费', '违约金', '违约金日期' if history == 'false' else '数据统计日期']
        data = make_excel_list(get_arrears(threshold, month, branch_office, history=history), fields)
        return excel.make_response_from_array(data, 'xlsx', file_name=file_name)


def get_available_memory():
    """
    获取当前服务器可用内存大小，单位为GB
    """
    pc_men = psutil.virtual_memory()
    div_gb_factor = (1024.0 ** 3)
    return float(pc_men.available / div_gb_factor)


def insert_into_mysql_qfshuju(data, count_done):
    """
    将欠费数据插入mysql数据库中
    """
    for d in data:
        branch_office = get_branch_office(str(d['YDDZ']))
        db.session.add(
            ArrearsData(yhbh=d['YHBH'], yhmc=d['YHMC'], yddz=d['YDDZ'], dfny=d['DFNY'], qf=d['QF'], yswyj=d['YSWYJ'],
                        sssj=d['SSSJ'], qfsc=d['QFSC'], wyjrq=d['WYJRQ'], fengxianzhi=None,
                        branch_office=branch_office))
    db.session.commit()
    current_app.logger.debug('成功插入' + str(count_done) + '行；')


def get_branch_office(address):
    address_list = ['莞城', '南城', '东城', '万江', '石碣', '石龙', '茶山', '石排', '企石', '横沥', '桥头', '谢岗',
                    '东坑', '常平', '寮步', '大朗', '黄江', '清溪', '塘厦', '凤岗', '长安', '虎门', '厚街', '沙田',
                    '道滘', '洪梅', '麻涌', '中堂', '高埗', '樟木头', '大岭山', '望牛墩', '松山湖']
    for d in address_list:
        if d in address:
            return d
    return '其他'


def call_stored_procedure():
    """
    调用存储过程，在mysql中建立几个关键表并插入数据
    """
    db.session.execute('call getQFZhiBiao_step1')
    db.session.execute('call getQFZhiBiao_step2')  # 获取欠费指标表，分两步完成
    current_app.logger.debug('成功完成qfzhibiao表的创建')
    db.session.execute('call getQFFengXian')  # 获取每个用户的历史风险数据
    current_app.logger.debug('成功完成qffengxian表的创建')
    db.session.execute('call add_fengxiangzhi_to_qfshuju')
    current_app.logger.debug('成功将fengxian值插入qfshuju表中')
    db.session.execute('call save_qfzhibiao')
    current_app.logger.debug('将历史qfzhibiao存入qfzhibiao_history表中')


@async
def first_sync(app):
    with app.app_context():
        cf = configparser.ConfigParser()
        path = app.config['SNYC_CONFIG_PATH']
        cf.read(path)
        try:
            cf.set('sync', 'SYNCHRONIZING', 'True')
            with open(path, 'w+') as f:
                cf.write(f)
            app.logger.debug('连接Oracle数据库')
            with cx_Oracle.connect(app.config['ORACLE_DATABASE_URI']) as my_db:
                cr = my_db.cursor()
                # sql = "SELECT COUNT(*) " \
                #       "from " \
                #       'sjcq.npmis_ZW_SSDFJL ' \
                #       "where to_char(SSSJ, 'yyyymmdd') > to_char(WYJRQ, 'yyyymmdd') and YSDF > 0 and " \
                #       "dfny >= (select to_char(add_months(sysdate, -36), 'yyyymm') from dual) and " \
                #       "DFNY <= (select to_char(add_months(sysdate, -1), 'yyyymm') from dual) "
                sql = "SELECT COUNT(*) " \
                      "from " \
                      'sjcq.npmis_ZW_SSDFJL ' \
                      "where to_char(SSSJ, 'yyyymmdd') > to_char(WYJRQ, 'yyyymmdd') and YSDF > 0"
                cr.execute(sql)
                rs1 = cr.fetchall()
                count = rs1[0][0]  # oracle满足条件的行数
                available_memory = get_available_memory()  # 服务器可用内存大小
                batch_size = int(available_memory * 50000)  # 每次处理行数
                batch_size = max(batch_size, 500000)
                n = int(math.ceil(count / batch_size))
                # 每次处理process_per行数据，n表示处理次数
                for i in range(n):
                    sql = 'SELECT * FROM (SELECT A.*, ROWNUM RN FROM (SELECT DISTINCT YHBH,YHMC,YDDZ,DFNY,QF,YSWYJ,' \
                          'FLOOR(SSSJ - WYJRQ) QFSC, WYJRQ,SSSJ FROM sjcq.npmis_ZW_SSDFJL ' \
                          ' WHERE TO_CHAR(SSSJ, \'yyyymmdd\') > TO_CHAR(WYJRQ, \'yyyymmdd\') AND YSDF > 0 ) A' \
                          ' WHERE ROWNUM <= ' + str((i + 1) * batch_size) + ') WHERE RN > ' + str(i * batch_size)

                    cr.execute(sql)
                    rs = cr.fetchall()
                    data = [{'YHBH': d[0], 'YHMC': d[1], 'YDDZ': d[2], 'DFNY': d[3],
                             'QF': d[4], 'YSWYJ': d[5], 'QFSC': d[6], 'WYJRQ': d[7], 'SSSJ': d[8]} for d in rs]
                    count_done = (i + 1) * batch_size if (i < n - 1) else count
                    insert_into_mysql_qfshuju(data, count_done)
                    app.logger.debug('同步进度{}%'.format((i + 1) / n * 100))
                cr.close()
                # my_db.close()
            app.logger.debug('数据同步完成，开始调用存储过程计算风险值')
            call_stored_procedure()  # 调用mysql中的存储过程
            # time.sleep(5)
            set_current_qf(app)
            # 发送邮件通知
            send_service_mail('数据库同步完成通知', app.config['ADMINS'],
                              'Full synchronization finished at {}, {} rows was synchronized'.format(
                                  datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), count), app=app)
            cf.set('sync', 'first_sync', 'True')
            cf.set('sync', 'SYNCHRONIZING', 'False')
            with open(path, 'w+') as f:
                cf.write(f)
        except Exception as e:
            app.logger.debug(e)
            send_service_mail('数据库同步错误通知', app.config['ADMINS'],
                              'Exception occurred at {}, detail: {}'.format(
                                  datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), e), app=app)
            sql = 'CALL TRUNCATE_TABLES'
            db.session.execute(sql)
        finally:
            cf.set('sync', 'SYNCHRONIZING', 'False')
            with open(path, 'w+') as f:
                cf.write(f)
