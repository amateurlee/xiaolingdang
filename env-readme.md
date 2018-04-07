#setup steps:
doc: https://blog.csdn.net/lihao21/article/details/47731903
- 安装配置nginx
```
  yum install nginx.x86_64
  nginx -s quit
  nginx
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
   supervisord -c config/supervisor.conf  #启动supervisor
   supervisorctl -c config/supervisor.conf reload|sstatus|tart [all]|[appname]
```
- 配置uWsgi、nginx
```
* 修改nginx配置：config/nginx.conf.bak (/etc/nginx/nginx.conf)
* 重启ngnix -s quit && nginx
* 停止gunicorn: kill -9 `ps ax |grep gunicorn |grep -v grep | awk '{print $1}'`
```


# 常用命令
## nginx
./nginx -s quit
./nginx
PersonalToken:ffdc61dcc96cb4517f0ba3f0fc4e3b419a76a71c
