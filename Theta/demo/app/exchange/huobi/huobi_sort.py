# -*- coding: utf-8 -*-

import time
import HuobiService
import pickle

huobi_currencys1 = ['ht', 'usdt', 'btc', 'bch', 'eth', 'xrp', 'ltc', 'ada', 'eos', 'xem', 'dash', 'neo', 'trx', 'icx',
                    'lsk', 'qtum', 'etc', 'btg', 'omg', 'hsr', 'zec', 'steem', 'bts', 'snt', 'salt', 'gnt', 'cmt',
                    'btm',
                    'pay', 'knc', 'powr', 'bat', 'dgd', 'ven', 'qash', 'zrx', 'gas', 'mana', 'eng', 'cvc', 'mco', 'mtl',
                    'rdn', 'storj', 'chat', 'srn', 'link', 'act', 'tnb', 'qsp', 'req', 'rpx', 'appc', 'rcn', 'smt',
                    'adx', 'tnt', 'ost', 'itc', 'lun', 'gnx', 'ast', 'evx', 'mds', 'snc', 'propy', 'eko', 'nas', 'bcd',
                    'wax', 'wicc', 'topc', 'swftc', 'dbc', 'elf', 'aidoc', 'qun', 'iost', 'yee', 'dat', 'theta', 'let',
                    'dta', 'utk', 'meet', 'zil', 'soc', 'ruff', 'ocn', 'ela', 'bcx', 'sbtc', 'etf', 'bifi', 'zla',
                    'stk',
                    'wpr', 'mtn', 'mtx', 'edu', 'blz', 'abt', 'ont', 'ctxc', 'bt1', 'bt2']

huobi_currencys = ['btcusdt', 'bchusdt', 'ethusdt', 'etcusdt', 'ltcusdt', 'eosusdt', 'xrpusdt', 'omgusdt', 'dashusdt',
                   'zecusdt', 'adausdt', 'ctxcusdt', 'actusdt', 'btmusdt', 'btsusdt', 'ontusdt', 'iostusdt', 'htusdt',
                   'trxusdt', 'dtausdt', 'neousdt', 'qtumusdt', 'elausdt', 'venusdt', 'thetausdt', 'sntusdt', 'zilusdt',
                   'xemusdt', 'nasusdt', 'ruffusdt', 'hsrusdt', 'letusdt', 'mdsusdt', 'storjusdt', 'elfusdt', 'itcusdt',
                   'cvcusdt', 'gntusdt', 'bchbtc', 'ethbtc', 'ltcbtc', 'etcbtc', 'eosbtc', 'omgbtc', 'xrpbtc',
                   'dashbtc', 'zecbtc', 'adabtc', 'btmbtc', 'ontbtc', 'iostbtc', 'htbtc', 'trxbtc', 'elabtc', 'wiccbtc',
                   'ocnbtc', 'zlabtc', 'abtbtc', 'mtxbtc', 'nasbtc', 'venbtc', 'dtabtc', 'neobtc', 'waxbtc', 'btsbtc',
                   'zilbtc', 'thetabtc', 'ctxcbtc', 'srnbtc', 'xembtc', 'edubtc', 'icxbtc', 'dgdbtc', 'chatbtc',
                   'wprbtc', 'lunbtc', 'swftcbtc', 'sntbtc', 'meetbtc', 'yeebtc', 'elfbtc', 'letbtc', 'qtumbtc',
                   'lskbtc', 'itcbtc', 'socbtc', 'qashbtc', 'mdsbtc', 'ekobtc', 'topcbtc', 'mtnbtc', 'actbtc', 'hsrbtc',
                   'stkbtc', 'storjbtc', 'gnxbtc', 'dbcbtc', 'sncbtc', 'cmtbtc', 'tnbbtc', 'ruffbtc', 'qunbtc',
                   'zrxbtc', 'kncbtc', 'blzbtc', 'propybtc', 'rpxbtc', 'appcbtc', 'aidocbtc', 'powrbtc', 'cvcbtc',
                   'paybtc', 'qspbtc', 'datbtc', 'rdnbtc', 'mcobtc', 'rcnbtc', 'manabtc', 'utkbtc', 'tntbtc', 'gasbtc',
                   'batbtc', 'ostbtc', 'linkbtc', 'gntbtc', 'mtlbtc', 'evxbtc', 'reqbtc', 'adxbtc', 'astbtc', 'engbtc',
                   'saltbtc', 'bifibtc', 'bcxbtc', 'bcdbtc', 'sbtcbtc', 'btgbtc', 'eoseth', 'omgeth', 'adaeth',
                   'zrxeth', 'asteth', 'knceth', 'onteth', 'hteth', 'btmeth', 'iosteth', 'elaeth', 'trxeth', 'abteth',
                   'naseth', 'ocneth', 'wicceth', 'zileth', 'ctxceth', 'zlaeth', 'wpreth', 'dtaeth', 'mtxeth',
                   'thetaeth', 'srneth', 'veneth', 'btseth', 'edueth', 'waxeth', 'hsreth', 'icxeth', 'mtneth', 'acteth',
                   'blzeth', 'qasheth', 'ruffeth', 'cmteth', 'elfeth', 'meeteth', 'soceth', 'qtumeth', 'itceth',
                   'swftceth', 'yeeeth', 'lsketh', 'luneth', 'leteth', 'gnxeth', 'chateth', 'ekoeth', 'topceth',
                   'dgdeth', 'stketh', 'mdseth', 'dbceth', 'snceth', 'payeth', 'quneth', 'aidoceth', 'tnbeth',
                   'appceth', 'rdneth', 'utketh', 'powreth', 'bateth', 'propyeth', 'manaeth', 'reqeth', 'cvceth',
                   'qspeth', 'evxeth', 'dateth', 'mcoeth', 'gnteth', 'gaseth', 'osteth', 'linketh', 'rcneth', 'tnteth',
                   'engeth', 'salteth', 'adxeth']


def huobi_sorts():  # 获取火币交易所数据
    # matrix = [['', 0, 0] for i in range(len(huobi_currencys) - 1)]  # marix是一个3 * n的二维数组，存储对应的货币 + 成交量 + 成交额
    matrix = []
    i = 0
    for currency in huobi_currencys:
            time.sleep(5)  # 1秒后再获取数据，限制十秒内请求100次
            info = dict()
            info["currency"] = currency  # 第一个元素存货币名称
            amounts = 0  # 成交量
            vols = 0.0  # 成交额
            counts = 0  # 成交笔数
            symbol = currency
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
                        counts += data["count"]
                    print(currency + "获取数据成功")
                else:
                    print(currency + "获取数据失败，返回数据为空")
            info["amounts"] = amounts
            info["vols"] = vols
            info["counts"] = counts
            matrix.append(info)
            # print(matrix[i])
            # print(" ")
            i = i + 1

    # 重新获取没有获取到的货币数据,尝试十次
    for n in range(1, 6):
        k = 0
        for row in matrix:
            if row["amounts"] == 0 and row["vols"] == 0 and row["counts"] == 0:
                time.sleep(5)  # 3秒后再获取数据，限制请求次数
                amounts = 0  # 成交量
                vols = 0.0  # 成交额
                counts = 0  # 成交笔数
                symbol = row["currency"]
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
                            counts += data["count"]
                        print(row["currency"] + "获取数据成功")
                    else:
                        print(row["currency"] + "获取数据失败，返回数据为空--重复第" + str(n) + "次")
                matrix[k]["amounts"] = amounts
                matrix[k]["vols"] = vols
                matrix[k]["counts"] = counts
            # print(matrix[k])
            # print(" ")
            k = k + 1

    print("原始matrix：")
    print(matrix)
    print(" ")

    sorted_by_amounts = sorted(matrix, key=lambda x: x['amounts'], reverse=True)
    pickle.dump(sorted_by_amounts, open("huobi_order_by_amounts.txt", "w"))
    print("按成交量amounts排序（降序）：")
    for row in sorted_by_amounts:
        print(row)
    print(" ")

    sorted_by_vols = sorted(matrix, key=lambda x: x['vols'], reverse=True)
    pickle.dump(sorted_by_vols, open("huobi_order_by_vols.txt", "w"))
    print("按成交额vols排序(降序)：")
    for row in sorted_by_vols:
        print(row)

    sorted_by_counts = sorted(matrix, key=lambda x: x['counts'], reverse=True)
    pickle.dump(sorted_by_counts, open("huobi_order_by_trades.txt", "w"))
    print("按成交额vols排序(降序)：")
    for row in sorted_by_counts:
        print(row)


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


if __name__ == "__main__":
    huobi_sorts()
