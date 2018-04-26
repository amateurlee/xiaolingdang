# -*- coding: UTF-8 -*-
from myapp.datacenter.db.models.indexTableCnModel import *
from myapp.datacenter.db.models.cnPERateTurnoverRate import *
from myapp.settings import *
import logging


class CnIndexDao:
    def __init__(self):
        pass

    def getCnIndexTableDataByStockCode(self, code):
        '''
        查询index_table_cn表(包括上证证指数和深圳成指)的数据, 支持所有数据和指定code获取数据的功能
        :param code:
        :return:
        '''
        if code:
            logging.debug("Get data from CnIndexTableCn table by stockcode:{}".format(STOCK_INFO["szzs"]["code"]))
            all_data = IndexTableCnModel.query.filter_by(stock_code=code).all()
        else:
            logging.debug("get ALL data from CnIndexTable")
            all_data = IndexTableCnModel.query.all()
        return all_data

    def getCnIndexTableDataCountByStockCode(self, code):
        '''
        根据code查询index_table_cn表指定code的记录数记录条数
        :param code:
        :return:
        '''
        count = IndexTableCnModel.query.filter_by(stock_code=code).count()
        return count

