# -*- coding: UTF-8 -*-
from myapp.datacenter.db.models.cnPERateTurnoverRateModel import *
from myapp.settings import *
import logging


class CnPeRurnoverRateDao:

    def getCnPeTurnoverRate(self, code):
        '''
        查询 cn_perate_turnoverrate 表(包括上证证指数和深圳成指)的市场平均PE和换手率数据, 支持所有数据和指定code获取数据的功能
        :param code:
        :return:
        '''
        if code:
            logging.debug("Get data from cn_perate_turnoverrate table by stockcode:{}".format(STOCK_INFO["szzs"]["code"]))
            all_data = CnPERateTurnoverRateModel.query.filter_by(stock_code=code).all()
        else:
            logging.debug("get ALL data from cn_perate_turnoverrate")
            all_data = CnPERateTurnoverRateModel.query.all()
        return all_data

    def addCnSSEPeTurnoverRateToDB(self):
        #TODO:

