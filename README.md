# Still in early stage dev

# Setup

## docker-compose

here is a example docker-compose.yml file you can use

```
services:
  backend:
    image: ghcr.io/mallo321123/openparcel:backend-release
    container_name: OpenParcel_backend
    ports:
      - "8080:8080"
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=a-nice-long-random-phrase
      - SECRET_KEY=a-nice-long-random-phrase
    depends_on:
      - mysql
      - redis
    networks:
      - OpenParcel

  frontend:
    image: ghcr.io/mallo321123/openparcel:frontend-release
    container_name: OpenParcel_frontend
    depends_on:
      - backend
    ports:
      - "3000:3000"
    networks:
      - OpenParcel

  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: a-nice-long-random-phrase
      MYSQL_DATABASE: OpenParcel
    command: --default-authentication-plugin=mysql_native_password
    ports:
      - "3306:3306"
    networks:
      - OpenParcel

  redis:
    container_name: redis
    image: redis:alpine
    ports:
      - "6379:6379"
    networks:
      - OpenParcel

networks:
  OpenParcel:
```

# Configuration

## Backend

### MYSQL_HOST

default: mysql

your mysql server adress

### MYSQL_PORT

default: 3306

your mysql port

### MYSQL_USER

default: root

your mysql user

### MYSQL_PASSWORD

your mysql password

### MYSQL_DATABASE

default: OpenParcel

your mysql database

### FLASK_PORT

default: 8080

the port your backend runs on. Change this only if you know what you do. 

all api requests are proxied through the frontend nginx server and directed to the default port

### SECRET_KEY

the secret key used to generate Login tokens, do not share

use a nice long random phrase

### REDIS_HOST

default: redis

your redis host adress

### REDIS_PORT

default: 6379

your redis port

### DEV_SERVER

default: false

when set to true, a flask server with advanced debugging will start

## Logging

when you want to recieve Server Logs, insert this into your volumes options:
```
- ./logs:/var/log/OpenParcel
```
replace ``` ./logs````with your logging directory