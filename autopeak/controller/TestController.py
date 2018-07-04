# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app

@app.route('/')
@app.route('/test')
def test():
    user = { 'nickname': 'Xihui_ControllerTest' } # fake user
    return render_template("test.html",
        title = 'Home',
        user = user)

@app.route('/test/<name>')
def paramTest(name):
    user = { 'nickname': name } # fake user
    return render_template("test.html",
        title = 'Home',
        user = user)
