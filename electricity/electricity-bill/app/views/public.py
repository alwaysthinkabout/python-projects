# -*- coding: utf-8 -*-
import configparser
import os

from flask import Blueprint, render_template, request, current_app
from app.extensions import excel

public = Blueprint('public', __name__)


@public.route('/')
@public.route('/index')
def index():
    path = current_app.config['SNYC_CONFIG_PATH']
    current_app.logger.debug(path)
    cf = configparser.ConfigParser()
    cf.read(path)
    first_sync = cf.getboolean('sync', 'FIRST_SYNC')
    synchronizing = cf.getboolean('sync', 'SYNCHRONIZING')
    return render_template('public/index.html', first_sync=first_sync, synchronizing=synchronizing)


@public.route('/risk')
def risk():
    user_no = request.args.get("user_no", "")
    name = request.args.get("name", "")
    return render_template('public/risk.html', user_no=user_no, name=name)


@public.route('/synchronizing')
def synchronizing():
    return render_template('public/synchronizing.html')


@public.route('/export')
def export():
    return excel.make_response_from_dict({'name': 'Jack', 'age': 12, 'gender': 'male'}, 'xlsx')
