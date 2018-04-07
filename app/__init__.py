# -*- coding: UTF-8 -*-

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

#只有在app对象之后声明，用于导入view模块
from app.controller import *
from app.controller import IndexController
