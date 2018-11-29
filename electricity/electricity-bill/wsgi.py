# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~~~~~~~~~~~

    Apache wsgi.

    :copyright: (c) 2018 by ymh.
    :date: 18/11/07
"""
activate_this = 'E:/server/venv3.6/Scripts/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

import sys

sys.path.insert(0, 'E:\github\project\electricity-bill')
from manage import app as application
