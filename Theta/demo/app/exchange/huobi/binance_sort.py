from binance.client import Client
import time
import pickle

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


client = Client("BuNN5Z0wbJUiEMXrVCQIRb8ZYZbXynocmKj3mELXSH5YxQXKlAn0yTShG5isui16",
                    "n8qXRSLmFKJhBbjvxoGitbKHJ4nfkcOZqtDWXe9p9CMFkhOqAPVjWByGyJ6ixRu2")
matrix = []
i = 0
for currency in binance_currencys:
        info = dict()
        info["currency"] = currency
        amounts = 0
        vols = 0.0
        try:
            datas = client.get_klines(symbol=currency, interval='1d')
        except:
            print(currency + "fail get_kline faile")
        else:
            if len(datas) > 0:
                # print("get" + currency + " information")
                for data in datas:
                    vols += float(data[5].encode('utf-8'))
                    amounts += data[8]
                # print(currency + " success")
            else:
                print(currency + " is null")
        info["trades"] = amounts
        info["vols"] = vols
        matrix.append(info)
        # print(matrix[i])
        # print(" ")
        i = i + 1

time.sleep(3.5)

for n in range(1, 11):
        k = 0
        for row in matrix:
            if row["trades"] == 0 and row["vols"] == 0:
                amounts = 0
                vols = 0.0
                symbol = row["currency"]
                try:
                    datas = client.get_klines(symbol=symbol, interval='1d')
                except:
                    print(row["currency"] + "fail , get_kline the " + str(n) + " times")
                else:
                    if len(datas) > 0:
                        # print("get " + row["currency"] + " info")
                        for data in datas:
                            vols += float(data[5].encode('utf-8'))
                            amounts += data[8]
                        # print(currency + " success")
                    else:
                        print(symbol + "fail the " + str(n) + " times")
                matrix[k]["trades"] = amounts
                matrix[k]["vols"] = vols
                # print(matrix[k])
                # print(" ")
            k = k + 1

print("origin matrix:")
# print(matrix)
print(" ")

sorted_by_trades = sorted(matrix, key=lambda x: x['trades'], reverse=True)
pickle.dump(sorted_by_trades, open("binance_order_by_trades.txt", "w"))
print("order by trades:")
for row in sorted_by_trades:
        print(row)
print(" ")

sorted_by_vols = sorted(matrix, key=lambda x: x['vols'], reverse=True)
pickle.dump(sorted_by_vols, open("binance_order_by_vols.txt", "w"))
print("order by vols:")
for row in sorted_by_vols:
        print(row)

