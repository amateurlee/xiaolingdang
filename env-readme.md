#setup steps:
doc: https://blog.csdn.net/lihao21/article/details/47731903
- 云主机配置
  配置ECS安全组（管理实例->安全组规则），开通入方向的80端口权限
- 安装配置nginx
```
  yum install nginx.x86_64
  nginx -s quit
  nginx
  #HTTPS config:
  sudo mkdir /etc/nginx/ssl
  #以下key不被浏览器认可
  sudo openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
  配置/etc/nginx/nginx.conf, 增加:
        listen       443 ssl;
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;
  # 通过 https://freessl.org 制造的key和pem 可以被认可
  
```
- python相关配置
```shell
   pip2.7 install virtualenv
   cd /root/xiaolingdang
   virtualenv --no-site-packages xiaolingdangvenv
   source ./xiaolingdangvenv/bin/activate
   pip install flask 
   pip install uwsgi
   ##python扩展包：
   pip install Flask-Script
   pip install gunicorn
   pip install supervisor
   echo_supervisord_conf > supervisor.conf   # 生成 supervisor 默认配置文件
   vim supervisor.conf                       # 修改 supervisor 配置文件，添加 gunicorn 进程管理
   supervisord -c config/supervisor.conf     #启动supervisor, 不执行supervisord命令的话，下一条会包没有sock文件或者socket.py的错误
   supervisorctl -c config/supervisor.conf reload|sstatus|tart [all]|[appname]
```
- 配置gunicorn、nginx
```
* 修改nginx配置：config/nginx.conf.bak (/etc/nginx/nginx.conf)
* 重启ngnix -s quit && nginx
* 停止gunicorn: kill -9 `ps ax |grep gunicorn |grep -v grep | awk '{print $1}'`
```
- 增加Firefox、Xvfb支持
```
* yum install firefox
* http://tobyho.com/2015/01/09/headless-browser-testing-xvfb/
* yum install python-xvfbwrapper.noarch xorg-x11-server-Xvfb.x86_64

```
# 常用命令
## nginx
./nginx -s quit
cp ./config/nginx.conf.bak /etc/nginx/nginx.conf
./nginx
PersonalToken:ffdc61dcc96cb4517f0ba3f0fc4e3b419a76a71c

# 设计思路

Web/app --> Controller --> services --> Dao --> Model --> DB
