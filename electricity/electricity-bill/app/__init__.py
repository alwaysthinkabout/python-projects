# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.extensions import cache, mail, excel
from app.tools import SSLSMTPHandler

db = SQLAlchemy()


def configure_extensions(app):
    mail.init_app(app)
    excel.init_excel(app)
    # cache.init_app(app)


def create_app(blueprints=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    from app import views
    from app import apis
    default_blueprints = (
        (views.public, ''),
        (views.test, '/test'),
        # apis
        (apis.v1, '/api/1')
    )
    if blueprints is None:
        blueprints = default_blueprints
    # Register blueprints
    configure_blueprints(app, blueprints)

    # Chain
    configure_extensions(app)
    configure_schedulers(app)
    # configure_logging(app)
    return app


def configure_logging(app):
    subject = '[Error] %s encountered errors on %s' % (app.config['DOMAIN'], datetime.now().strftime('%Y/%m/%d'))
    subject += (' [DEV]' if app.debug else '')
    mail_config = [(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                   app.config['MAIL_DEFAULT_SENDER'], app.config['ADMINS'],
                   subject,
                   (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])]
    if app.config['MAIL_USE_SSL']:
        mail_handler = SSLSMTPHandler(*mail_config)
    else:
        mail_handler = SMTPHandler(*mail_config)

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    formatter = logging.Formatter(
        '%(asctime)s %(process)d-%(thread)d %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    debug_file_handler = TimedRotatingFileHandler(debug_log, when='midnight', interval=1, backupCount=90)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, app.config['ERROR_LOG'])
    error_file_handler = TimedRotatingFileHandler(error_log, when='midnight', interval=1, backupCount=90)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    # Flask运行在产品模式时, 只会输出ERROR, 此处使之输入INFO
    if not app.config['DEBUG']:
        app.logger.setLevel(logging.INFO)


def configure_blueprints(app, blueprints):
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_schedulers(app):
    from app.jobs import init_schedule
    init_schedule(app)
