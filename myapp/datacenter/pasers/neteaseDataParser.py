# -*- coding: UTF-8 -*-
import json
class NeteaseDataParser:
    def __init__(self):
        pass

    def parseAllData(self, jsonStr):
        '''
        解析网页数据，返回dict结构数据
        :param jsonStr:
                {
                    "closes": [
                        3163.86,
                        3136.44,
                        3146.56
                    ],
                    "symbol": "000001",
                    "times": [
                        "20180402",
                        "20180403",
                        "20180404"
                    ],
                    "name": "上证指数"
                }
        :return:
        '''
        resultDict = json.loads(jsonStr)
