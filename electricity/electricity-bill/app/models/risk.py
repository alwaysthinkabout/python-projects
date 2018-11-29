# -*- coding: utf-8 -*-
from app import db


class Risk(db.Model):
    __tablename__ = 'qffengxian'

    yhbh = db.Column(db.String(60), primary_key=True)
    fengxianzhi = db.Column(db.Float(3))
    bill_month = db.Column(db.String(60))


# class HistoricalRisk(db.Model):
#     __tablename__ = 'qffengxian'
#
#     id = db.Column(db.Integer, primary_key=True)
#     yhbh = db.Column(db.String(60))
#     fengxianzhi = db.Column(db.Float(3))
#     dfny = db.Column(db.String(60))
