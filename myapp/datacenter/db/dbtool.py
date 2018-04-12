# -*- coding: UTF-8 -*-
from myapp.datacenter.db.models.indexTableCnModel import *
from myapp.settings import *
import logging


class DBTool:
    def __init__(self):
        pass

    def getIndexTableCnAllData(self):
        logging.debug("get data from IndexTable...")
        all_data = IndexTableCnModel.query.all()
        # all_data = IndexTableCnModel.IndexTableCnModel.query.filter_by(id=1).all()
        return all_data

    def getIndexTableCnDataByStockCode(self, code):
        '''
        根据stock_code查询数据
        :param code:
        :return:
        '''
        logging.debug("Get data from IndexTableCn table by stockcode:{}".format(STOCK_INFO["szzs"]["code"]))
        all_data = IndexTableCnModel.query.filter_by(stock_code=code).all()
        return all_data

    def getIndexTableCnDataCountByStockCode(self, code):
        '''
        根据code查询记录条数
        :param code:
        :return:
        '''
        count = IndexTableCnModel.query.filter_by(stock_code=code).count()
        return count