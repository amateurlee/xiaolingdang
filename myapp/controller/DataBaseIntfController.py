# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app
from myapp.datacenter.db.dbtool import DBTool

@app.route('/getFullData/cn/all')
def getFullDataCnAll():
    '''
        获取所有A股数据包的数据
    '''
    dbTool = DBTool()
    data = dbTool.getIndexTableCnData()
    return render_template("cnAlldata.html", data = data)


