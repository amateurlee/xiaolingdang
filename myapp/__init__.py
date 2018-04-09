# -*- coding: UTF-8 -*-
import logging
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy

from myapp.settings import *

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(filename)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= APP_PATH+'/myapp.log',
                filemode='w')

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

#配置数据库地址
logging.info("init database:"+settings.SQLITE3_DATA_PATH)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLITE3_DATA_PATH
#该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
xld_db = SQLAlchemy(app)

#只有在app对象之后声明，用于导入view模块
from controller import TestController
from controller import IndexController
from controller import DataBaseIntfController

