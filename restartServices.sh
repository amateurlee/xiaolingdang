#!/bin/sh
rootPath=/root/xiaolingdang
#nginx -s quit
#cp config/nginx.conf.bak /etc/nginx/nginx.conf
cd ${rootPath} && supervisorctl -c config/supervisor.conf reload
#nginx
