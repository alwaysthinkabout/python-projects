# -*- coding: utf-8 -*-

from flask_caching import Cache
from flask_mail import Mail
import flask_excel as excel


__all__ = ['mail', 'cache', 'excel']

mail = Mail()
cache = Cache()

