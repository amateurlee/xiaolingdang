# -*- coding: UTF-8 -*-
from flask import render_template
from .. import app

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': '^_^' } # fake user
    return render_template("index.html",
        title = 'AutoPeak automation framework',
        user = user)

