# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app
from myapp.datacenter.db.dbtool import DBTool

@app.route('/getFullData/ag')
def getFullData():
    user = { 'nickname': '^_^' } # fake user
    dbTool = DBTool()
    data = dbTool.getIndexTableCnData()
    return render_template("IndexModelData.html", data = data)


