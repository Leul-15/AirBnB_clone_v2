#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

apt-get update
apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html/;
    index  index.html;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /error_404.html;
    location /404 {
        root /var/www/html/;
        internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
