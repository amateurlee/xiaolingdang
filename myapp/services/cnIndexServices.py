# -*- coding: UTF-8 -*-

from myapp.datacenter.dataSource.neteaseFetcher import NeteaseDataFetcher
from myapp.datacenter.dataSource.sseDataSource import SseDataSource
from myapp.datacenter.db.dao.cnindexdao import CnIndexDao
from myapp.datacenter.db.dao.cnPeTurnoverRateDao import CnPeRurnoverRateDao
from myapp.datacenter.db.models import indexTableCnModel
from myapp import xld_db
from myapp.settings import *


class CnIndexServices:
    '''
    CnDataCenterServices提供A股市场的逻辑处理业务
    '''

    def __init__(self):
        self.neteaseDataFetcher = NeteaseDataFetcher()
        self.sseDataSource = SseDataSource()
        self.cnIndexDao = CnIndexDao()
        self.cnPeRurnoverRateDao = CnPeRurnoverRateDao()

    def fetchCnIndexDataFromWeb(self, stock_code, addtime=None):
        '''
        从页面获取数据
        :param stock_code:
        :param addtime:
        :return:
        '''
        if not addtime:
            data = self.neteaseDataFetcher.getDataAllData(stockcode=stock_code, period=NeteaseDataFetcher.period["day"],
                                                          stocktype=NeteaseDataFetcher.stocktype["index"])
            return data
        else:
            # TODO: 获取某一个时间点的数据
            pass

    def countCnIndexDataByCode(self, code):
        return self.cnIndexDao.getCnIndexTableDataCountByStockCode(code=code)

    def addCnIndexDataToDB(self, webData):
        '''
        将指数数据添加到数据库，添加之前首先判断是否有重复的数据，去重后添加， index_table_cn表中的数据可以以stock_code和time作为唯一标示
        :param retData:
        :return:
        '''

        ###### 1. 从数据库读取数据

        szzsData = self.cnIndexDao.getCnIndexTableDataByStockCode(STOCK_INFO["szzs"]["code"])
        searchIndexData = {}  # 仅用来保存key
        modelDataList = []
        if szzsData:
            for data in szzsData:
                uniKey = "{}{}".format(data.stock_code, data.time)
                searchIndexData[uniKey] = 0 # 以指数代码和时间组成唯一标示的key判断存在性
        ###### 2. 遍历新数据，判断是否已经在数据库中存在，添加新数据
        for wdata in webData:
            if searchIndexData.has_key("{}{}".format(wdata["stock_code"], wdata["time"])):
                continue  # 数据库中已经存在当前时间的记录
            else:
                model = indexTableCnModel.IndexTableCnModel(index_name=wdata["index_name"],
                                                            stock_code=wdata["stock_code"],
                                                            time=wdata["time"], close=wdata["close"])
                modelDataList.append(model)
        ###### 3. 添加数据
        self.cnIndexDao.addToDB(modelDataList)

    def getCnPeRurnoverRateFromWeb (self, startDate, endData):
        '''
        从SSE上证交易所获取平均PE和换手率
        :param startDate: "2018-04-01"
        :param endData: "2018-04-04"
        :return:
        '''
        sse = SseDataSource()
        data = sse.getSSEPERatio(beginDate=startDate, toDate=endData)
        self.assertTrue(len(data) > 0)
        # formerdata = data.pop(0)
        # self.assertTrue(formerdata[1]!=None, "PE data is none for:{}".format(formerdata))
        # self.assertTrue(formerdata[2]!=None, "TurnOver data is none for:{}".format(formerdata))
        for d in data:
            self.assertTrue(d[1] != None, "PE data is none for:{}".format(d))
            self.assertTrue(d[2] != None, "TurnOver data is none for:{}".format(d))
            self.assertNotEqual("{}{}".format(d[1], d[2]), "{}{}".format(formerdata[1], formerdata[2]))
        self.test_PERatioTurnOverRateDataToDB(data)


