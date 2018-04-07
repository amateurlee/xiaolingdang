#!/bin/sh
rootPath=/root/xiaolingdang
#nginx -s quit
cd ${rootPath} && supervisorctl -c config/supervisor.conf reload
#nginx
