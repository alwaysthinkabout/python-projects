# -*- coding: utf-8 -*-
"""
    jobs
    ~~~~~~~~~~~~~~

    Jobs defined here.

    :copyright: (c) 2016 by fengweimin.
    :date: 16/8/12
"""

import os
import threading
import time
from collections import Counter

import schedule


from app.models import Post
from app.views.public import kline_binance_new, kline_huobi_new

post_view_times_counter = Counter()



def update_view_times(app):
    """
    Update view times for posts.
    """
    app.logger.info('Scheduler update_view_times running: %s' % post_view_times_counter)
    d = dict(post_view_times_counter)
    post_view_times_counter.clear()
    for k, v in d.iteritems():
        p = Post.find_one({'_id': k})
        if p:
            try:
                p.viewTimes += v
                p.save()
            except:
                app.logger.exception('Failed when updating the viewTime for album %s' % p._id)


def huobi_update_prices(app):
    """
    Update view times for posts.
    """
    app.logger.info('Scheduler update_prices running: %s' % post_view_times_counter)
    try:
        kline_huobi_new(app)
    except:
        app.logger.exception('Failed when updating the huobi prices')


def binance_update_prices(app):
    """
    Update view times for posts.
    """
    app.logger.info('Scheduler update_prices running: %s' % post_view_times_counter)
    try:
        kline_binance_new(app)
    except:
        app.logger.exception('Failed when updating binance the prices')


def run_schedule(app):
    """
    Invoke schedule.
    """
    # For schedule rules please refer to https://github.com/dbader/schedule
    schedule.every(20).minutes.do(update_view_times, app)

    # schedule.every(0.5).minutes.do(huobi_update_prices, app)

    # schedule.every(5).minutes.do(binance_update_prices, app)

    while True:
        schedule.run_pending()
        time.sleep(1)


def init_schedule(app):
    """
    Init.
    """
    # http://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode/
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        t = threading.Thread(target=run_schedule, args=(app,))
        # Python threads don't die when the main thread exits, unless they are daemon threads.
        t.setDaemon(True)
        t.start()
