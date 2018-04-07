# -*- coding: UTF-8 -*-

# gunicorn -w 4 -b 127.0.0.1:8000 myapp:app

from myapp import app

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
