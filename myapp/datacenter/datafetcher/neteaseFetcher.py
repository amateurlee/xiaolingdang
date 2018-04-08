# -*- coding: UTF-8 -*-
from myapp.services.commonTool import CommonTool

class NeteaseDataFetcher:
    period = {"day": "day", "week": "week", "month": "month"}
    stockrightprice = {"kline": "klinederc", "klinederc": "klinederc"}
    stocktype = {"index": 0, "stock": 1}

    def __init__(self):
        self.stockcode = 000001

        # http://img1.money.126.net/data/[沪深拼音]/[是否复权]/[周期]/times/[股票代码].jso
        # http://img1.money.126.net/data/hs/kline/day/times/0000300.json
        self.allDataUrl = "http://img1.money.126.net/data/hs/kline/{period}/times/{stocktype}{stockcode}.json"

    def getDataAllData(self, stockcode, period, stocktype, stockrightprice = stockrightprice["kline"]):
        '''

        :param stockcode:
        :param period:
        :param stocktype:
        :param stockrightprice:
        :return:
        '''
        self.allDataUrl = self.allDataUrl.format(period = period, stocktype=stocktype, stockcode=stockrightprice)
        return CommonTool.doGet(self.allDataUrl)