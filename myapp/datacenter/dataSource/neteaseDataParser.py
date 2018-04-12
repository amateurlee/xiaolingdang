# -*- coding: UTF-8 -*-
import json, logging

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
        :return: [{记录1}{记录2}]
        '''
        resultDict = json.loads(jsonStr)
        if not resultDict or len(resultDict["times"])<=0 or len(resultDict["times"])!= len(resultDict["closes"]):
            logging.error("Web data parse failed, data is illegal:{}".format(resultDict))
            return False
        parsedDataList = []
        for i in xrange(len(resultDict["times"])):
            parsedData = {} # 转换成index_table_cn表结构格式， index_name, stock_code, time, close
            parsedData["index_name"] = resultDict["name"]
            parsedData["stock_code"] = resultDict["symbol"]
            parsedData["time"] = resultDict["times"][i]
            parsedData["close"] = resultDict["closes"][i]
            parsedDataList.append(parsedData)

        return parsedDataList
