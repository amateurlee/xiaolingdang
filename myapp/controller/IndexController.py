# -*- coding: UTF-8 -*-
from flask import render_template
from ..myapp import app

@app.route('/index')
def main():
    user = { 'nickname': 'Xihui_ControllerTest' } # fake user
    return render_template("index.html",
        title = 'Home',
        user = user)
