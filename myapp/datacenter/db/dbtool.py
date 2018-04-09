# -*- coding: UTF-8 -*-
from myapp.datacenter.db.models import IndexTableCnModel
import logging

class DBTool:
    def __init__(self):
        pass

    def getIndexTableCnData(self):
    	logging.debug("get data from IndexTable...")
        all_data = IndexTableCnModel.IndexTableCnModel.query.all()
        #all_data = IndexTableCnModel.IndexTableCnModel.query.filter_by(id=1).all()

        return all_data
