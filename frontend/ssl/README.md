Place your ssl certificate and key this directory.

generate dhparam.pem: openssl dhparam -out frontend/ssl/dhparam.pem 2048
generate crt and key: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout frontend/ssl/nginx.key -out frontend/ssl/nginx.crt