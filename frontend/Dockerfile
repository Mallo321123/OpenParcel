FROM nginx:alpine

# Kopiere Nginx-Konfiguration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Kopiere die statischen Dateien ins Web-Verzeichnis
COPY src/ /usr/share/nginx/html

COPY ssl /etc/nginx/ssl

# Exponiere den Standard-Nginx-Port
EXPOSE 80
EXPOSE 443

# Starte Nginx
CMD ["nginx", "-g", "daemon off;"]