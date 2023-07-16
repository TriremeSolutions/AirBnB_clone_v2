#!/usr/bin/env bash
# Script configures Nginx server for web_static deployment

apt-get update -y
apt-get install -y nginx

service nginx start
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Test HTML Page!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen      80 default_server;
    listen      [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root        /var/www/html;
    index       world.html world.php world.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index world.html world.htm world.php;
    }
    
    location /redirect_me {
        return 301 http://github.com/TriremeSolutions/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
exit 0
