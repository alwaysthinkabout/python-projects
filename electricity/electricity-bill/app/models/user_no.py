# -*- coding: utf-8 -*-
from app import db


class TDQZYH(db.Model):
    __tablename__ = 'tdqzyh'

    yhbh = db.Column(db.String(60), primary_key=True)
