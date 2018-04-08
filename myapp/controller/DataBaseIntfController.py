# -*- coding: UTF-8 -*-
from flask import render_template
from myapp import app, services
from myapp.datacenter.db.dbtool import DBTool

@app.route('/getFullData/ag/<indexCode>')
def index(indexCode):
    user = { 'nickname': '^_^' } # fake user
    dbTool = DBTool()
    data = dbTool.getIndexTableCnData()
    return render_template("IndexModelData.html", data = data)
