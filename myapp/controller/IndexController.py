# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Xihui_ControllerTest' } # fake user
    return render_template("index.html",
        title = 'Home',
        user = user)

@app.route('/index/<name>')
def param(name):
    user = { 'nickname': name } # fake user
    return render_template("index.html",
        title = 'Home',
        user = user)
