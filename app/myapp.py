# -*- coding: UTF-8 -*-

# gunicorn -w 4 -b 127.0.0.1:8000 myapp:app

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/testapi")
def helloapi():
    return "Hello api!"

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
