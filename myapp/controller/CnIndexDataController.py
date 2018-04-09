# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app
from myapp.datacenter.db.dbtool import DBTool
from myapp.services.cnDataCenterServices import *

@app.route('/getFullData/cn/all')
def getFullDataCnAll():
    '''
        获取所有A股数据包的数据
    '''
    dbTool = DBTool()
    data = dbTool.getIndexTableCnAllData()
    return render_template("cn/cnAlldata.html", data = data)

@app.route('/cn/addIndex')
def addCnData():
    '''
        向数据库补充一code的所有数据
    '''
    return render_template("cn/cnAddData.html")

@app.route('/cn/addIndex/<stock_code>')
def addCnData(stock_code):
    '''
    向数据库补充某一code下所有的数据
    :param stock_code:
    :param addtime:
    :return: 添加是否成功
    '''

    cnDataService = CnDataCenterServices()
    # 从页面获取指标数据
    retData = cnDataService.fetchCnIndexDataFromWeb(STOCK_INFO["szzs"]["code"])


    # 将页面获取的数据保存到数据库中
    countBefore = cnDataService.countCnIndexDataByCode(STOCK_INFO["szzs"]["code"])
    ret = cnDataService.addCnIndexDataToDB(retData)
    countAfter = cnDataService.countCnIndexDataByCode(STOCK_INFO["szzs"]["code"])

    cnDataService = CnDataCenterServices()
    # 从页面获取指标数据
    retData = cnDataService.fetchCnIndexDataFromWeb(stock_code)
    if not retData or len(retData) == 0:
        return False
    # 将页面获取的数据保存到数据库中
    ret = cnDataService.addCnIndexDataToDB(retData)
    if not ret:
        return False

    return True

@app.route('/cn/addIndex/<stock_code>/<addtime>')
def complementIndexCnData(stock_code,addtime):
    '''
    补充某个时间点、某个指数的
    :param stock_code:
    :param addtime:
    :return:
    '''
    #TODO:
    pass