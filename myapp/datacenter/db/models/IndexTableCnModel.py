# -*- coding: UTF-8 -*-
from myapp import xld_db
from myapp.datacenter.db.models.baseModel import BaseModel

class IndexTableCnModel(xld_db.Model, BaseModel):  #,UserMixin) UserMixin是Flask-Login库中所需要的
    __tablename__ = 'index_table_cn'
    # 每个属性定义一个字段
    id = xld_db.Column(xld_db.Integer, primary_key=True)
    index_name = xld_db.Column(xld_db.String(64))
    stock_code = xld_db.Column(xld_db.String(64))
    time = xld_db.Column(xld_db.String(64))
    closes = xld_db.Column(xld_db.Float)

    def __repr__(self):
        return '<Index name %r>' % self.index_name
