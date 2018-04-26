# -*- coding: UTF-8 -*-
import unittest, os
from myapp.services.cnIndexServices import *
from myapp.settings import *


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        # Do something to initiate the test environment here.
        pass

    def tearDown(self):
        # Do something to clear the test environment here.
        pass

    def test_FetchCnIndexData(self):
        cnDataService = CnIndexServices()
        # 从页面获取指标数据
        retData = cnDataService.fetchCnIndexDataFromWeb(STOCK_INFO["szzs"]["code"])
        self.assertTrue(retData != False)
        self.assertTrue(len(retData) > 0)

        # 将页面获取的数据保存到数据库中
        countBefore = cnDataService.countCnIndexDataByCode(STOCK_INFO["szzs"]["code"])
        #Just for test# ret = cnDataService.addCnIndexDataToDB(retData)
        countAfter = cnDataService.countCnIndexDataByCode(STOCK_INFO["szzs"]["code"])
        self.assertTrue(countAfter >= countBefore)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
