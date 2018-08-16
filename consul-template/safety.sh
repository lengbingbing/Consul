#!/bin/bash
ps -ef | grep nginx | grep -v grep | awk '{print $2}' | xargs kill -9
/usr/local/openresty/nginx/sbin/nginx  -c /usr/local/job/server.conf
echo done!


