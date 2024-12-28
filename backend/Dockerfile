FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

# Dev mode option
CMD if [ "$DEV_SERVER" = "false" ]; then \
        exec gunicorn --bind 0.0.0.0:8080 openapi_server.__main__:app; \
    else \
        exec python3 -m openapi_server; \
    fi