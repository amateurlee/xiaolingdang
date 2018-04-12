# -*- coding: UTF-8 -*-
from myapp import xld_db
import logging


class CnPERateTurnoverRateModel(xld_db.Model):  # ,UserMixin) UserMixin是Flask-Login库中所需要的
    ''' 记录中国市场整体市盈率和换手率， 分为上证指数000001， 深证整个市场、深圳中小板、和深圳创业板
    CREATE TABLE cn_perate_turnoverrate (
    id            INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL,
    stock_code    TEXT    NOT NULL,
    date          TEXT    NOT NULL,
    pe_rate       REAL,
    turnover_rate REAL
    );
    '''
    __tablename__ = 'cn_perate_turnoverrate'
    # 每个属性定义一个字段
    id = xld_db.Column(xld_db.Integer, primary_key=True)
    stock_code = xld_db.Column(xld_db.String(64))
    date = xld_db.Column(xld_db.String(64))
    pe_rate = xld_db.Column(xld_db.Float)
    turnover_rate = xld_db.Column(xld_db.Float)
    logging.debug("initing CN PERate TurnOver Rate...")

    def __init__(self, stock_code, date, pe_rate, turnover_rate):
        self.stock_code = stock_code
        self.date = date
        self.pe_rate = pe_rate
        self.turnover_rate = turnover_rate

    def __repr__(self):
        return '<Index code %r>' % self.stock_code
