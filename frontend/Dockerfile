FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY src/ /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]