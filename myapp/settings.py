# -*- coding: UTF-8 -*-
import os

APP_PATH = os.path.abspath(os.path.dirname(__file__))
SQLITE3_DATA_PATH = "sqlite:///{rootPath}/datacenter/db/autopeak.sqlite3".format(rootPath=APP_PATH)

STOCK_INFO = {
    "szzs": {"code": "000001", "name": "上证指数"}
}
