# -*- coding: utf-8 -*-
"""
    blog
    ~~~~~~~~~~~~~~

    Blog pages/actions.

    :copyright: (c) 2016 by fengweimin.
    :date: 16/8/16
"""

from datetime import datetime
import time
from binance.client import Client

import pymongo
from bson.objectid import ObjectId
from flask import Blueprint, request, render_template, abort, jsonify, current_app
from flask_babel import gettext as _
from flask_login import current_user, login_required

from app.jobs import post_view_times_counter
from app.models import Post, Tag, User
from app.mongosupport import Pagination, populate_model
from app.tools import send_support_email
from app.tools.decorators import user_not_rejected, user_not_evil
from app.models import Price
import HuobiService
import HuobiUtil
import datetime
import time

blog = Blueprint('blog', __name__)

PAGE_COUNT = 10
# client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
# "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")

huobi_currencys = ['ht', 'usdt', 'btc', 'bch', 'eth', 'xrp', 'ltc', 'ada', 'eos', 'xem', 'dash', 'neo', 'trx', 'icx',
                   'lsk', 'qtum', 'etc', 'btg', 'omg', 'hsr', 'zec', 'steem', 'bts', 'snt', 'salt', 'gnt', 'cmt', 'btm',
                   'pay', 'knc', 'powr', 'bat', 'dgd', 'ven', 'qash', 'zrx', 'gas', 'mana', 'eng', 'cvc', 'mco', 'mtl',
                   'rdn', 'storj', 'chat', 'srn', 'link', 'act', 'tnb', 'qsp', 'req', 'rpx', 'appc', 'rcn', 'smt',
                   'adx', 'tnt', 'ost', 'itc', 'lun', 'gnx', 'ast', 'evx', 'mds', 'snc', 'propy', 'eko', 'nas', 'bcd',
                   'wax', 'wicc', 'topc', 'swftc', 'dbc', 'elf', 'aidoc', 'qun', 'iost', 'yee', 'dat', 'theta', 'let',
                   'dta', 'utk', 'meet', 'zil', 'soc', 'ruff', 'ocn', 'ela', 'bcx', 'sbtc', 'etf', 'bifi', 'zla', 'stk',
                   'wpr', 'mtn', 'mtx', 'edu', 'blz', 'abt', 'ont', 'ctxc', 'bt1', 'bt2']


@blog.route('/')
@blog.route('/index')
def index():
    """
    Index.
    """
    tid = request.args.get('t', None)
    page = int(request.args.get('p', 1))
    start = (page - 1) * PAGE_COUNT
    condition = {}
    if tid:
        condition = {'tids': ObjectId(tid)}
    count = Post.count(condition)
    cursor = Post.find(condition, skip=start, limit=PAGE_COUNT, sort=[('createTime', pymongo.DESCENDING)])
    pagination = Pagination(page, PAGE_COUNT, count)
    return render_template('blog/index.html', posts=list(cursor), pagination=pagination, tags=all_tags())


def all_tags():
    """
    Fetch all tags.
    """
    cursor = Tag.find({}, sort=[('weight', pymongo.DESCENDING)])
    return [t for t in cursor]


@blog.route('/post/<ObjectId:post_id>')
def post(post_id):
    """
    Post.
    """
    p = Post.find_one({'_id': post_id})
    if not p:
        abort(404)

    post_view_times_counter[post_id] += 1

    uids = set()
    for c in p.comments:
        uids.add(c.uid)
        for r in c.replys:
            uids.add(r.uid)
    user_dict = {u._id: u for u in User.find({'_id': {'$in': list(uids)}})}
    return render_template('blog/post.html', id=post_id, post=p, tags=all_tags(), user_dict=user_dict)


@blog.route('/post/new', methods=('GET', 'POST'))
@blog.route('/post/change/<ObjectId:post_id>', methods=('GET', 'POST'))
@login_required
@user_not_rejected
def new(post_id=None):
    # Open page
    if request.method == 'GET':
        p = None
        # Change
        if post_id:
            p = Post.find_one({'_id': post_id})
            if not p:
                abort(404)

        return render_template('blog/new.html', post=p, tags=all_tags())
    # Handle post request
    else:
        try:
            post = populate_model(request.form, Post)
            if not post.title:
                return jsonify(success=False, message=_('Post title can not be blank!'))
            if not post.body:
                return jsonify(success=False, message=_('Post body can not be blank!'))
            if not post.tids:
                return jsonify(success=False, message=_('Post must at least have a tag!'))

            # New
            if not post_id:
                post.uid = current_user._id
                post.save()
                post_id = post._id
                current_app.logger.info('Successfully new a post %s' % post._id)
            # Change
            else:
                existing = Post.find_one({'_id': post_id})
                existing.title = post.title
                existing.tids = post.tids
                existing.body = post.body
                existing.save()
                current_app.logger.info('Successfully change a post %s' % post._id)
        except:
            current_app.logger.exception('Failed when saving post')
            return jsonify(success=False, message=_('Failed when saving the post, please try again later!'))

        return jsonify(success=True, message=_('Save the post successfully.'), pid=str(post_id))


@blog.route('/comment/<ObjectId:post_id>', methods=('POST',))
@login_required
@user_not_rejected
@user_not_evil
def comment(post_id):
    """
    评论博文.
    """
    post = Post.find_one({'_id': post_id})
    if not post:
        return jsonify(success=False, message=_('The post does not exist!'))

    content = request.form.get('content', None)
    if not content or not content.strip():
        return jsonify(success=False, message=_('Comment content can not be blank!'))

    max = -1
    for c in post.comments:
        if max < c.id:
            max = c.id

    now = datetime.now()

    cmt = {
        'id': max + 1,
        'uid': current_user._id,
        'content': content,
        'time': now
    }

    post.comments.insert(0, cmt)
    post.save()

    send_support_email('comment()',
                       u'New comment %s on post %s.' % (content, post._id))

    return jsonify(success=True, message=_('Save comment successfully.'))


@blog.route('/reply/<ObjectId:post_id>/<int:comment_id>', methods=('POST',))
@login_required
@user_not_rejected
@user_not_evil
def reply(post_id, comment_id):
    """
    回复.
    """
    post = Post.find_one({'_id': post_id})
    if not post:
        return jsonify(success=False, message=_('The post does not exist!'))

    content = request.form.get('content', None)
    if not content or not content.strip():
        return jsonify(success=False, message=_('Reply content can not be blank!'))

    cmt = next((c for c in post.comments if c.id == comment_id), -1)
    if cmt == -1:
        return jsonify(success=False, message=_('The comment you would like to reply does not exist!'))

    now = datetime.now()

    reply = {
        'uid': current_user._id,
        'rid': ObjectId(request.form.get('rid', None)),
        'content': content,
        'time': now
    }

    cmt.replys.append(reply)
    post.save()

    send_support_email('reply()', u'New reply %s on post %s.' % (content, post._id))

    return jsonify(success=True, message=_('Save reply successfully.'))


@blog.route('/get/kline_binance', methods=('GET', 'POST'))
def kline_binance():  # 获取binance交易所数据
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    datas = client.get_klines(symbol="LTCBTC", interval="1d")
    for data in datas:
        # 依据日期和交易所名称判断是否在数据库中重复
        existing_ex = Price.find_one({'ex': unicode("binance")})
        existing_date = Price.find_one(
            {'date': unicode(datetime.datetime.utcfromtimestamp(data[0] / 1000).strftime("%Y/%m/%d"))})
        # print('existing:', exiting)
        if not existing_ex or not existing_date:
            price = Price()
            price.date = unicode(datetime.datetime.utcfromtimestamp(data[0] / 1000).strftime("%Y/%m/%d"))
            price.open = float(data[1].encode('utf-8'))
            price.close = float(data[4].encode('utf-8'))
            price.lowest = float(data[3].encode('utf-8'))
            price.highest = float(data[2].encode('utf-8'))
            # price.createTime = datetime.datetime.today()
            price.ex = unicode("binance")
            price.save()
    return jsonify(success=True, message=_('Save the post successfully.'))


# 将unicode字典转化为字符字典
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


@blog.route('/get/kline_huobi', methods=('GET', 'POST'))
def kline_huobi():  # 获取火币交易所数据
    symbol = "btcusdt"
    period = "1day"
    udata = HuobiService.get_kline(symbol, period, 100)  # 返回的key和value是unicode
    datas = byteify(udata)['data']  # 将unicode的key和value转为string
    for data in datas:
        # 依据日期和交易所名称判断是否在数据库中重复
        existing_ex = Price.find_one({'ex': unicode("huobi")})
        existing_date = Price.find_one({'date': unicode(time.strftime('%Y-%m-%d', time.localtime(data['id'])))})
        # print('existing:', exiting)
        if not existing_ex or not existing_date:
            price = Price()
            price.date = unicode(time.strftime('%Y-%m-%d', time.localtime(data['id'])))
            price.open = float(data['open'])
            price.close = float(data['close'])
            price.lowest = float(data['low'])
            price.highest = float(data['high'])
            price.ex = unicode("huobi")
            price.save()
            print('price.date', price.date)
    return jsonify(success=True, message=_('Save the post successfully.'))


# 获取火币所有币种
@blog.route('/get/kline_huobi_currencys', methods=('GET', 'POST'))
def kline_huobi_currencys():  # 获取火币交易所数据
    url = HuobiUtil.MARKET_URL + '/v1/common/currencys'
    params = {}
    udata = HuobiUtil.http_get_request(url, params)  # 返回的key和value是unicode
    datas = byteify(udata)['data']  # 将unicode的key和value转为string
    print(datas)
    return jsonify(success=True, message=_('Save the post successfully.'))
