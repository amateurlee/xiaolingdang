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
   # ./yum -y install python-devel python-setuptools libxml2-devel
```
- 配置uWsgi、nginx
```
* 增加uwsgi配置：config/uwsgi.ini
* 修改nginx配置：config/nginx.conf.bak (/etc/nginx/nginx.conf)
* 启动uWsgi： uwsgi –ini config/uwsgi.ini
* 重启ngnix -s quit && nginx
* 停止nWsgi: kill -9 `ps ax |grep uWSGI |grep -v grep | awk '{print $1}'`
    uwsgi --stop uwsgi/uwsgi.pid && uwsgi --ini config/uwsgi.ini
```


# 常用命令
## nginx
./nginx -s quit
./nginx

