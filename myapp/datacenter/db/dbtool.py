# -*- coding: UTF-8 -*-
from myapp.datacenter.db.models import IndexTableCnModel

class DBTool:
    def __init__(self):
        pass

    def getIndexTableCnData(self):
        all_data = IndexTableCnModel.query.all()
        # all_data = IndexTableCnModel.query.filter_by(id=1).all()

        return all_data
