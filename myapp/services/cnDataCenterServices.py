# -*- coding: UTF-8 -*-

from myapp.datacenter.dataSource.neteaseFetcher import *
from myapp.datacenter.db.dbtool import DBTool
from myapp.datacenter.db.models import IndexTableCnModel
from myapp import xld_db
from myapp.settings import *


class CnDataCenterServices:
    '''
    CnDataCenterServices提供A股市场的逻辑处理业务
    '''

    def __init__(self):
        self.neteaseDataFetcher = NeteaseDataFetcher()
        self.dbTool = DBTool()

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
        return self.dbTool.getIndexTableCnDataCountByStockCode(code=code)

    def addCnIndexDataToDB(self, webData):
        '''
        将指数数据添加到数据库，添加之前首先判断是否有重复的数据，去重后添加， index_table_cn表中的数据可以以stock_code和time作为唯一标示
        :param retData:
        :return:
        '''

        ###### 1. 从数据库读取数据

        szzsData = self.dbTool.getIndexTableCnDataByStockCode(STOCK_INFO["szzs"]["code"])
        searchIndexData = {}  # 仅用来保存key
        modelDataList = []
        if szzsData:
            for data in szzsData:
                searchIndexData[data.time] = 0
        ###### 2. 遍历新数据，判断是否已经在数据库中存在，添加新数据
        for wdata in webData:
            if searchIndexData.has_key(wdata["time"]):
                continue  # 数据库中已经存在当前时间的记录
            else:
                model = IndexTableCnModel.IndexTableCnModel(index_name=wdata["index_name"],
                                                            stock_code=wdata["stock_code"],
                                                            time=wdata["time"], close=wdata["close"])
                modelDataList.append(model)
        ###### 3. 添加数据
        if len(modelDataList) > 0:
            for model in modelDataList:
                xld_db.session.add(model)
            xld_db.session.commit()
