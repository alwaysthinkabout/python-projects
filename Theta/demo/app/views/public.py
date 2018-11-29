# -*- coding: utf-8 -*-
"""
    public.py
    ~~~~~~~~~~~~~~

    Public pages/actions.

    :copyright: (c) 2016 by fengweimin.
    :date: 16/5/12
"""

from flask import Blueprint, render_template, current_app, session, redirect, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, login_required
from flask_principal import identity_changed, Identity, AnonymousIdentity
from flask_wtf import Form
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email

from app.models import User, Price
from app.tools import send_support_email
import pymongo

from binance.client import Client
import HuobiService
import datetime
import time

public = Blueprint('public', __name__)

huobi_currencys = ['ht', 'usdt', 'btc', 'bch', 'eth', 'xrp', 'ltc', 'ada', 'eos', 'xem', 'dash', 'neo', 'trx', 'icx',
                   'lsk', 'qtum', 'etc', 'btg', 'omg', 'hsr', 'zec', 'steem', 'bts', 'snt', 'salt', 'gnt', 'cmt', 'btm',
                   'pay', 'knc', 'powr', 'bat', 'dgd', 'ven', 'qash', 'zrx', 'gas', 'mana', 'eng', 'cvc', 'mco', 'mtl',
                   'rdn', 'storj', 'chat', 'srn', 'link', 'act', 'tnb', 'qsp', 'req', 'rpx', 'appc', 'rcn', 'smt',
                   'adx', 'tnt', 'ost', 'itc', 'lun', 'gnx', 'ast', 'evx', 'mds', 'snc', 'propy', 'eko', 'nas', 'bcd',
                   'wax', 'wicc', 'topc', 'swftc', 'dbc', 'elf', 'aidoc', 'qun', 'iost', 'yee', 'dat', 'theta', 'let',
                   'dta', 'utk', 'meet', 'zil', 'soc', 'ruff', 'ocn', 'ela', 'bcx', 'sbtc', 'etf', 'bifi', 'zla', 'stk',
                   'wpr', 'mtn', 'mtx', 'edu', 'blz', 'abt', 'ont', 'ctxc', 'bt1', 'bt2']

binance_currencys = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BCCBTC',
                     'GASBTC', 'BNBETH', 'BTCUSDT', 'ETHUSDT', 'HSRBTC', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH',
                     'MCOBTC', 'WTCBTC', 'WTCETH', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'OMGETH',
                     'ZRXBTC', 'ZRXETH', 'STRATBTC', 'STRATETH', 'SNGLSBTC', 'SNGLSETH', 'BQXBTC', 'BQXETH', 'KNCBTC',
                     'KNCETH', 'FUNBTC', 'FUNETH', 'SNMBTC', 'SNMETH', 'NEOETH', 'IOTABTC', 'IOTAETH', 'LINKBTC',
                     'LINKETH', 'XVGBTC', 'XVGETH', 'SALTBTC', 'SALTETH', 'MDABTC', 'MDAETH', 'MTLBTC', 'MTLETH',
                     'SUBBTC', 'SUBETH', 'EOSBTC', 'SNTBTC', 'ETCETH', 'ETCBTC', 'MTHBTC', 'MTHETH', 'ENGBTC', 'ENGETH',
                     'DNTBTC', 'ZECBTC', 'ZECETH', 'BNTBTC', 'ASTBTC', 'ASTETH', 'DASHBTC', 'DASHETH', 'OAXBTC',
                     'ICNBTC', 'BTGBTC', 'BTGETH', 'EVXBTC', 'EVXETH', 'REQBTC', 'REQETH', 'VIBBTC', 'VIBETH', 'HSRETH',
                     'TRXBTC', 'TRXETH', 'POWRBTC', 'POWRETH', 'ARKBTC', 'ARKETH', 'YOYOETH', 'XRPBTC', 'XRPETH',
                     'MODBTC', 'MODETH', 'ENJBTC', 'ENJETH', 'STORJBTC', 'STORJETH', 'BNBUSDT', 'VENBNB', 'YOYOBNB',
                     'POWRBNB', 'VENBTC', 'VENETH', 'KMDBTC', 'KMDETH', 'NULSBNB', 'RCNBTC', 'RCNETH', 'RCNBNB',
                     'NULSBTC', 'NULSETH', 'RDNBTC', 'RDNETH', 'RDNBNB', 'XMRBTC', 'XMRETH', 'DLTBNB', 'WTCBNB',
                     'DLTBTC', 'DLTETH', 'AMBBTC', 'AMBETH', 'AMBBNB', 'BCCETH', 'BCCUSDT', 'BCCBNB', 'BATBTC',
                     'BATETH', 'BATBNB', 'BCPTBTC', 'BCPTETH', 'BCPTBNB', 'ARNBTC', 'ARNETH', 'GVTBTC', 'GVTETH',
                     'CDTBTC', 'CDTETH', 'GXSBTC', 'GXSETH', 'NEOUSDT', 'NEOBNB', 'POEBTC', 'POEETH', 'QSPBTC',
                     'QSPETH', 'QSPBNB', 'BTSBTC', 'BTSETH', 'BTSBNB', 'XZCBTC', 'XZCETH', 'XZCBNB', 'LSKBTC', 'LSKETH',
                     'LSKBNB', 'TNTBTC', 'TNTETH', 'FUELBTC', 'FUELETH', 'MANABTC', 'MANAETH', 'BCDBTC', 'BCDETH',
                     'DGDBTC', 'DGDETH', 'IOTABNB', 'ADXBTC', 'ADXETH', 'ADXBNB', 'ADABTC', 'ADAETH', 'PPTBTC',
                     'PPTETH', 'CMTBTC', 'CMTETH', 'CMTBNB', 'XLMBTC', 'XLMETH', 'XLMBNB', 'CNDBTC', 'CNDETH', 'CNDBNB',
                     'LENDBTC', 'LENDETH', 'WABIBTC', 'WABIETH', 'WABIBNB', 'LTCETH', 'LTCUSDT', 'LTCBNB', 'TNBBTC',
                     'TNBETH', 'WAVESBTC', 'WAVESETH', 'WAVESBNB', 'GTOBTC', 'GTOETH', 'GTOBNB', 'ICXBTC', 'ICXETH',
                     'ICXBNB', 'OSTBTC', 'OSTETH', 'OSTBNB', 'ELFBTC', 'ELFETH', 'AIONBTC', 'AIONETH', 'AIONBNB',
                     'NEBLBTC', 'NEBLETH', 'NEBLBNB', 'BRDBTC', 'BRDETH', 'BRDBNB', 'MCOBNB', 'EDOBTC', 'EDOETH',
                     'WINGSBTC', 'WINGSETH', 'NAVBTC', 'NAVETH', 'NAVBNB', 'LUNBTC', 'LUNETH', 'TRIGBTC', 'TRIGETH',
                     'TRIGBNB', 'APPCBTC', 'APPCETH', 'APPCBNB', 'VIBEBTC', 'VIBEETH', 'RLCBTC', 'RLCETH', 'RLCBNB',
                     'INSBTC', 'INSETH', 'PIVXBTC', 'PIVXETH', 'PIVXBNB', 'IOSTBTC', 'IOSTETH', 'CHATBTC', 'CHATETH',
                     'STEEMBTC', 'STEEMETH', 'STEEMBNB', 'NANOBTC', 'NANOETH', 'NANOBNB', 'VIABTC', 'VIAETH', 'VIABNB',
                     'BLZBTC', 'BLZETH', 'BLZBNB', 'AEBTC', 'AEETH', 'AEBNB', 'RPXBTC', 'RPXETH', 'RPXBNB', 'NCASHBTC',
                     'NCASHETH', 'NCASHBNB', 'POABTC', 'POAETH', 'POABNB', 'ZILBTC', 'ZILETH', 'ZILBNB', 'ONTBTC',
                     'ONTETH', 'ONTBNB', 'STORMBTC', 'STORMETH', 'STORMBNB', 'QTUMBNB', 'QTUMUSDT', 'XEMBTC', 'XEMETH',
                     'XEMBNB', 'WANBTC', 'WANETH', 'WANBNB', 'WPRBTC', 'WPRETH', 'QLCBTC', 'QLCETH', 'SYSBTC', 'SYSETH',
                     'SYSBNB', 'QLCBNB', 'GRSBTC', 'GRSETH', 'ADAUSDT', 'ADABNB', 'CLOAKBTC', 'CLOAKETH']

binance_matrix = []  # 存储币安各币种的成交量和成交额


@public.route('/blank')
def blank():
    """
    Blank page.
    """
    return render_template('public/blank.html')


@public.route('/styleguide')
def styleguide():
    """
    Blank page.
    """
    return render_template('public/styleguide.html')


# ----------------------------------------------------------------------------------------------------------------------
# Login/Signup
#

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember')
    next_url = HiddenField('next')


@public.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login.
    """
    form = LoginForm()

    if form.validate_on_submit():
        em = form.email.data.strip().lower()
        u = User.find_one({'email': em})
        if not u or not check_password_hash(u.password, form.password.data):
            return render_template('public/login.html', form=form, error=_('User name or password incorrect!'))

        # Keep the user info in the session using Flask-Login
        login_user(u)

        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(), identity=Identity(u.get_id()))

        next_url = form.next_url.data
        if not next_url:
            next_url = '/'
        return redirect(next_url)

    next_url = request.args.get('next', '')
    form.next_url.data = next_url
    return render_template('public/login.html', form=form)


@public.route('/logout')
@login_required
def logout():
    """
    Logout.
    """
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect("/")


class SignupForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    repassword = PasswordField('repassword', validators=[DataRequired()])
    agree = BooleanField('agree', validators=[DataRequired(_('Please agree our service policy!'))])


@public.route('/signup', methods=('GET', 'POST'))
def signup():
    """
    Signup.
    """
    form = SignupForm()

    if form.validate_on_submit():
        if not form.password.data == form.repassword.data:
            return render_template('public/signup.html', form=form, error=_('Password dismatch!'))

        em = form.email.data.strip().lower()
        u = User.find_one({'email': em})
        if u:
            return render_template('public/signup.html', form=form, error=_('This email has been registered!'))

        u = User()
        u.email = em
        u.password = unicode(generate_password_hash(form.password.data.strip()))
        u.name = u.email.split('@')[0]
        u.save()

        current_app.logger.info('A new user created, %s' % u)
        send_support_email('signup()', u'New user %s with id %s.' % (u.email, u._id))

        # Keep the user info in the session using Flask-Login
        login_user(u)

        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(), identity=Identity(u.get_id()))

        return redirect('/')

    return render_template('public/signup.html', form=form)


@public.route('/')
def index():
    """
    Index page.
    """
    cursor = Price.find({}, sort=[('date', pymongo.ASCENDING)])
    prices = [[c.date, c.open, c.close, c.lowest, c.highest] for c in cursor]
    current_app.logger.info('Found %s prices' % len(prices))
    return render_template('public/index.html', prices=prices)


def kline_binance_new(app):
    kline_binance()


@public.route('/get/kline_binance', methods=('GET', 'POST'))
def kline_binance():  # 获取binance交易所数据
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    datas = client.get_klines(symbol="LTCBTC", interval="1d")
    print("获取binance数据")
    for data in datas:
        print(data)
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
    # return jsonify(success=True, message=_('Save the post successfully.'))


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


def kline_huobi_new(app):
    kline_huobi()

@public.route('/get/kline_huobi', methods=('GET', 'POST'))
def kline_huobi():  # 获取火币交易所数据
    symbol = "btcusdt"
    period = "1day"
    udata = HuobiService.get_kline(symbol, period, 100)  # 返回的key和value是unicode
    datas = byteify(udata)['data']  # 将unicode的key和value转为string
    print("获取huobi数据")
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
            # price.createTime = datetime.datetime.today()
            price.ex = unicode("huobi")
            price.save()
            # print('price.date', price.date)
    print("end")
    # return jsonify(success=True, message=_('Save the post successfully.'))


@public.route('/get/huobi_sort', methods=('GET', 'POST'))
def huobi_sorts():  # 获取火币交易所数据
    # matrix = [['', 0, 0] for i in range(len(huobi_currencys) - 1)]  # marix是一个3 * n的二维数组，存储对应的货币 + 成交量 + 成交额
    matrix = []  # 一维数组，元素未字典，存储货币名称 + 成交量 + 成交额
    i = 0
    for currency in huobi_currencys:
        if currency == 'usdt':
            continue
        else:
            time.sleep(3)  # 1秒后再获取数据，限制十秒内请求100次
            info = dict()
            info["currency"] = currency  # 第一个元素存货币名称
            amounts = 0  # 成交量
            vols = 0.0  # 成交额
            symbol = currency + "usdt"
            try:
                udata = HuobiService.get_kline(symbol, '1day', 30)  # 返回的key和value是unicode
            except:
                print(currency + "获取数据失败，get_kline函数执行异常")
            else:
                if udata.has_key('data'):
                    datas = byteify(udata)['data']  # 将unicode的key和value转为string
                    print("获取" + currency + "的数据")
                    for data in datas:
                        vols += data['vol']  # 第二个元素存成交量
                        amounts += data['amount']  # 第三个元素存成交额
                    print(currency + "获取数据成功")
                else:
                    print(currency + "获取数据失败，返回数据为空")
            info["amounts"] = amounts
            info["vols"] = vols
            matrix.append(info)
            print(matrix[i])
            print(" ")
            i = i + 1

    # 重新获取没有获取到的货币数据,尝试十次
    for n in range(1, 11):
        k = 0
        for row in matrix:
            if row["amounts"] == 0 and row["vols"] == 0:
                time.sleep(3)  # 3秒后再获取数据，限制请求次数
                amounts = 0  # 成交量
                vols = 0.0  # 成交额
                symbol = row["currency"] + "usdt"
                try:
                    udata = HuobiService.get_kline(symbol, '1day', 30)  # 返回的key和value是unicode
                except:
                    print(row["currency"] + "获取数据失败,get_kline函数执行异常--重复第" + str(n) + "次")
                else:
                    if udata.has_key('data'):
                        datas = byteify(udata)['data']  # 将unicode的key和value转为string
                        print("获取" + row["currency"] + "的数据")
                        for data in datas:
                            vols += data['vol']  # 第二个元素存成交量
                            amounts += data['amount']  # 第三个元素存成交额
                        print(currency + "获取数据成功")
                    else:
                        print(currency + "获取数据失败，返回数据为空--重复第" + str(n) + "次")
                matrix[k]["amounts"] = amounts
                matrix[k]["vols"] = vols
                print(matrix[k])
                print(" ")
            k = k + 1

    print("原始matrix：")
    print(matrix)
    print(" ")

    sorted_by_amounts = sorted(matrix, key=lambda x: x['amounts'], reverse=True)
    print("按成交量amounts排序（降序）：")
    for row in sorted_by_amounts:
        print(row)
    print(" ")

    sorted_by_vols = sorted(matrix, key=lambda x: x['vols'], reverse=True)
    print("按成交额vols排序(降序)：")
    for row in sorted_by_vols:
        print(row)
    return jsonify(success=True, message=_('Save the post successfully.'))


@public.route('/get/kline_binance/currencys', methods=('GET', 'POST'))
def get_binance_currencys():  # 获取binance交易所所有货币
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    datas = byteify(client.get_all_tickers())
    currencys = []
    for data in datas:
        currencys.append(data["symbol"])
    print(currencys)
    return jsonify(success=True, message=_('Save the post successfully.'))


@public.route('/get/binance_sort', methods=('GET', 'POST'))
def binance_sorts():  # 获取火币交易所数据
    # matrix = [['', 0, 0] for i in range(len(huobi_currencys) - 1)]  # marix是一个3 * n的二维数组，存储对应的货币 + 成交量 + 成交额
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    matrix = []  # 一维数组，元素为字典，存储货币名称 + 成交量 + 成交额
    i = 0
    for currency in binance_currencys:
        info = dict()
        info["currency"] = currency  # 第一个元素存货币名称
        amounts = 0  # 成交量
        vols = 0.0  # 成交额
        try:
            datas = client.get_klines(symbol=currency, interval='1d')
        except:
            print(currency + "获取数据失败，get_kline函数执行异常")
        else:
            if len(datas) > 0:
                print("获取" + currency + "的数据")
                for data in datas:
                    vols += float(data[9].encode('utf-8'))  # 第二个元素存成交量
                    amounts += data[6]  # 第三个元素存成交额
                print(currency + "获取数据成功")
            else:
                print(currency + "获取数据失败，返回数据为空")
        info["amounts"] = amounts
        info["vols"] = vols
        matrix.append(info)
        print(matrix[i])
        print(" ")
        i = i + 1

    time.sleep(3.5)  # 3.5秒后再尝试重新获取数据

    # 重新获取没有获取到的货币数据,尝试十次
    for n in range(1, 11):
        k = 0
        for row in matrix:
            if row["amounts"] == 0 and row["vols"] == 0:
                amounts = 0  # 成交量
                vols = 0.0  # 成交额
                symbol = row["currency"]
                try:
                    datas = client.get_klines(symbol=symbol, interval='1d')
                except:
                    print(row["currency"] + "获取数据失败,get_kline函数执行异常--重复第" + str(n) + "次")
                else:
                    if len(datas) > 0:
                        print("获取" + row["currency"] + "的数据")
                        for data in datas:
                            vols += float(data[9].encode('utf-8'))  # 第二个元素存成交量
                            amounts += data[6]  # 第三个元素存成交额
                        print(currency + "获取数据成功")
                    else:
                        print(symbol + "获取数据失败，返回数据为空--重复第" + str(n) + "次")
                matrix[k]["amounts"] = amounts
                matrix[k]["vols"] = vols
                print(matrix[k])
                print(" ")
            k = k + 1

    print("原始matrix：")
    print(matrix)
    print(" ")

    sorted_by_amounts = sorted(matrix, key=lambda x: x['amounts'], reverse=True)
    print("按成交量amounts排序（降序）：")
    for row in sorted_by_amounts:
        print(row)
    print(" ")

    sorted_by_vols = sorted(matrix, key=lambda x: x['vols'], reverse=True)
    print("按成交额vols排序(降序)：")
    for row in sorted_by_vols:
        print(row)

    return jsonify(success=True, message=_('Save the post successfully.'))


# 初始化binance_matrix数组
@public.route('/get/binance_sort_by_historical_trade', methods=('GET', 'POST'))
def binance_sorts_by_historical_trade():  # 获取火币交易所数据
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    print("进入binance_sorts_by_historical_trade")
    binance_matrix = []
    for currency in binance_currencys:
        info = dict()
        dates = []  # 存储每个日期的交易额和交易量，日期单位为天
        amounts = 0.0  # 总的交易量
        vols = 0.0  # 总的交易额
        info["currency"] = currency
        try:
            time.sleep(0.5)
            datas = client.get_historical_trades(symbol=currency)
        except:
            print("获取" + currency + "信息失败，get_historical_trades出错")
            info["amounts"] = amounts
            info["vols"] = vols
            info["fromId"] = -1  # id为-1，表示获取该货币信息的时候出现异常，需要下次重新获取
            info["dates"] = dates
        else:
            if len(datas) > 0:
                # print("获取到" + currency + "信息")
                for data in datas:
                    qty = float(data["qty"].encode('utf-8'))
                    price = float(data["price"].encode('utf-8'))
                    amounts += qty
                    vols += qty * price
                    if len(dates) > 0:  # dates不为空时
                        # 当前记录对应的日期已经存在dates里面，则修改该日期对应的交易额和交易量即可,
                        if dates[len(dates) - 1]["date"] == time.strftime('%Y-%m-%d', time.localtime(data['time'] / 1000)):
                            dates[len(dates) - 1]["amounts"] += qty
                            dates[len(dates) - 1]["vols"] += qty * price
                            # print("date已存在")
                        else:
                            row_tmp = dict()
                            row_tmp["date"] = time.strftime('%Y-%m-%d',
                                                            time.localtime(data['time'] / 1000))  # dates中没有当前记录的日期时，则将其新增进去
                            row_tmp["amounts"] = qty
                            row_tmp["vols"] = qty * price
                            dates.append(row_tmp)
                            # print("新增一个date 1")
                    else:  # 当dates为空时，则直接将当前记录新增进去
                        row_tmp = dict()
                        row_tmp["date"] = time.strftime('%Y-%m-%d', time.localtime(data['time'] / 1000))
                        row_tmp["amounts"] = qty
                        row_tmp["vols"] = qty * price
                        dates.append(row_tmp)
                        # print("新增一个date 2")

                info["amounts"] = amounts
                info["vols"] = vols
                info["fromId"] = datas[len(datas) - 1]["id"]  # 获取到的最大的id
            else:
                print(currency + "信息为空，返回为空")
                info["amounts"] = amounts
                info["vols"] = vols
                info["fromId"] = -1  # 获取到的最大的id
                info["dates"] = dates
        # 每一个币种对应一个dates数组，按天记录了该币种的交易额和交易量，dates格式为：[{date: 2018-4-2, amounts: 4444444.00, vols: 999200.0}]
        info["dates"] = dates
        binance_matrix.append(info)

    print("原始binance_matrix)：")
   # print(binance_matrix)
    print(" ")

    sorted_by_amounts = sorted(binance_matrix, key=lambda x: x['amounts'], reverse=True)
    print("按成交量amounts排序（降序）：")
    for row in sorted_by_amounts:
        print(row)
    print(" ")

    sorted_by_vols = sorted(binance_matrix, key=lambda x: x['vols'], reverse=True)
    print("按成交额vols排序(降序)：")
    for row in sorted_by_vols:
        print(row)
    get_binance_amount_vols_period(300)  # 之后以5分钟为周期周期性获取最新消息
    return jsonify(success=True, message=_('Save the post successfully.'))


def get_binance_amount_vols_period(period):
    print("开始实时获取新的数据")
    print(" ")
    # while True:
    time.sleep(period)  # 以period为周期周期性获取信息
    for row in binance_matrix:
        symbol = row["currency"]
        fromId = row["fromId"]
        get_binance_amounts_vols_by_symbol(symbol, fromId)

def get_binance_amounts_vols_by_symbol(symbol, fromId):
    client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
    try:
        if fromId == -1:  # 代表目前数组里面还没有当前币种的信息
            time.sleep(0.5)
            datas = client.get_historical_trades(symbol=symbol)
        else:  # 从当前数组中该币种最大的id记录开始搜索
            time.sleep(0.5)
            datas = client.get_historical_trades(symbol=symbol, fromId=fromId)
    except:
        print("获取" + symbol + "信息失败，get_historical_trades出错")
    else:
        if len(datas) > 0:
            for row in binance_matrix:  # 找到该币种然后把amounts和vols加上去，并修改dates
                if row["currency"] == symbol:
                    for data in datas:
                        qty = float(data["qty"].encode('utf-8'))
                        price = float(data["price"].encode('utf-8'))
                        row["amount"] += qty
                        row["vols"] += qty * price
                        # 修改该币种的dates数组
                        if len(row["dates"]) > 0:  # dates不为空时
                            if row["dates"][len(row["dates"]) - 1]["date"] == time.strftime('%Y-%m-%d', time.localtime(
                                    data['time'])):  # 当前记录对应的日期已经存在dates里面，则修改该日期对应的交易额和交易量即可,
                                row["dates"][len(row["dates"]) - 1]["amounts"] += qty
                                row["dates"][len(row["dates"]) - 1]["vols"] += qty * price
                            else:
                                row_tmp = dict()
                                row_tmp["date"] = time.strftime('%Y-%m-%d',
                                                                time.localtime(data['time']))  # dates中没有当前记录的日期时，则将其新增进去
                                row_tmp["amounts"] = qty
                                row_tmp["vols"] = qty * price
                                row["dates"].append(row_tmp)
                        else:  # 当dates为空时，则直接将当前记录新增进去
                            row_tmp = dict()
                            row_tmp["date"] = time.strftime('%Y-%m-%d', time.localtime(data['time']))
                            row_tmp["amounts"] = qty
                            row_tmp["vols"] = qty * price
                            row["dates"].append(row_tmp)
                    row["fromId"] = datas[len(datas) - 1]["id"]  # 获取到的最大的id
                break

    print("原始matrix：")
    # print(binance_matrix)
    print(" ")

    sorted_by_amounts = sorted(binance_matrix, key=lambda x: x['amounts'], reverse=True)
    print("更新后按成交量amounts排序（降序）：")
    for row in sorted_by_amounts:
        print(row)
    print(" ")

    sorted_by_vols = sorted(binance_matrix, key=lambda x: x['vols'], reverse=True)
    print("更新后按成交额vols排序(降序)：")
    for row in sorted_by_vols:
        print(row)
