# -*- coding: UTF-8 -*-
from myapp.tools.commonTool import CommonTool
from myapp.datacenter.dataSource.neteaseDataParser import NeteaseDataParser


class NeteaseDataFetcher:
    period = {"day": "day", "week": "week", "month": "month"}
    stockrightprice = {"kline": "kline", "klinederc": "klinederc"}
    stocktype = {"index": 0, "stock": 1}

    def __init__(self):
        self.parser = NeteaseDataParser()
        # http://img1.money.126.net/data/[沪深拼音]/[是否复权]/[周期]/times/[股票代码].jso
        # http://img1.money.126.net/data/hs/kline/day/times/0000300.json
        self.allDataUrl = "http://img1.money.126.net/data/hs/{stockrightprice}/{period}/times/{stocktype}{stockcode}.json"

    def getDataAllData(self, stockcode, period, stocktype, stockrightprice=stockrightprice["kline"]):
        ''' 根据指定参数获取数据
        :param stockcode:
        :param period: day, week, month
        :param stocktype: index:0, stock: 1
        :param stockrightprice:
        :return: data after parser
        '''
        self.allDataUrl = self.allDataUrl.format(stockcode=stockcode, period=period, stocktype=stocktype,
                                                 stockrightprice=stockrightprice)
        alldata = CommonTool.doGet(self.allDataUrl)
        # 必要的数据转换
        alldataparsed = self.parser.parseAllData(alldata)
        return alldataparsed
