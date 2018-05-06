# -*- coding: UTF-8 -*-
import unittest, os
from myapp.datacenter.dataSource.sseDataSource import SseDataSource
import myapp.datacenter.dataSource

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        # Do something to initiate the test environment here.
        pass

    def tearDown(self):
        # Do something to clear the test environment here.
        pass

    def test_FetchCNPeToRateDataFromWeb(self):
        ''' 测试上证指数PE和换手率获取 '''
        sse = SseDataSource()
        data = sse.getSSEPERatio(beginDate="2018-04-01", toDate="2018-04-04")
        self.assertTrue(len(data)>0)
        # formerdata = data.pop(0)
        # self.assertTrue(formerdata[1]!=None, "PE data is none for:{}".format(formerdata))
        # self.assertTrue(formerdata[2]!=None, "TurnOver data is none for:{}".format(formerdata))
        for d in data:
            self.assertTrue(d[1] != None, "PE data is none for:{}".format(d))
            self.assertTrue(d[2] != None, "TurnOver data is none for:{}".format(d))
            self.assertNotEqual("{}{}".format(d[1], d[2]), "{}{}".format(formerdata[1], formerdata[2]))
        self._PERatioTurnOverRateDataToDB(data)


    def _PERatioTurnOverRateDataToDB(self, data):
        '''
        测试数据添加到数据库
        :return:
        '''
        pass #peToRate =
