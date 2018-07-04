# -*- coding: UTF-8 -*-

#supervisorctl -c config/supervisor.conf reload

from myapp import app

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
