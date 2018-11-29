from datetime import datetime

import cx_Oracle
from flask import current_app

from app import db


def test_oracle(app):
    with app.app_context():
        my_db = cx_Oracle.connect(current_app.config['ORACLE_DATABASE_URI'])
        cr = my_db.cursor()
        # 找出当月欠费用户的编号
        sql = "SELECT YHBH FROM SJCQ.NPMIS_ZW_QFJL WHERE dfny=(SELECT TO_CHAR(SYSDATE, 'yyyymm') FROM DUAL)"
        cr.execute(sql)
        rs = cr.fetchall()
        rs = [r[0] for r in rs]
        print(rs)


def test_get_records_num(app):
    with app.app_context():
        my_db = cx_Oracle.connect(current_app.config['ORACLE_DATABASE_URI'])
        cr = my_db.cursor()
        start = datetime.now()
        # 找出当月欠费用户的编号
        sql = "SELECT YHBH FROM SJCQ.NPMIS_ZW_QFJL WHERE dfny=(SELECT TO_CHAR(SYSDATE, 'yyyymm') FROM DUAL)"
        cr.execute(sql)
        rs = cr.fetchall()
        rs = [r[0] for r in rs]
        print("time1:", datetime.now() - start)
        # # MySQL里查询符合条件的用户编号（有重复）
        rr = db.session.execute('SELECT YHBH FROM qfshuju').fetchall()
        print("time2:", datetime.now() - start)
        result = [r[0] for r in rr]
        filtered = list(filter(lambda x: x in rs, result))
        print("time3:", datetime.now() - start)
        print(len(filtered))
