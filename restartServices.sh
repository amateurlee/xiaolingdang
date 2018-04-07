#!/bin/sh
rootPath=/root/xiaolingdang
nginx -s quit
uwsgi --stop ${rootPath}/logs/uwsgi.pid 
uwsgi --ini ${rootPath}/config/uwsgi.ini
nginx
