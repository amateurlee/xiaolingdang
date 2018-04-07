#!/bin/sh
rootPath=/root/xiaolingdang
uwsgi --stop ${rootPath}/logs/uwsgi.pid 
uwsgi --ini ${rootPath}/config/uwsgi.ini
