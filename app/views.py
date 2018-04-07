# -*- coding: UTF-8 -*-
from flask import render_template
from myapp import app

@app.route('/main')
def main():
    user = { 'nickname': 'Xihui' } # fake user
    return render_template("index.html",
        title = 'Home',
        user = user)
