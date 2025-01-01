from flask_wtf.csrf import CSRFProtect
import os
import logging
from logging.handlers import RotatingFileHandler


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    WTF_CSRF_ENABLED = True

csrf = CSRFProtect()


LOG_DIR = '/var/log/OpenParcel'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING_LEVEL = logging.INFO

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "secret")
JWT_IDENTITY_CLAIM = "user"
JWT_TOKEN_LOCATION = "cookies"
JWT_ACCESS_COOKIE_NAME = "access_token"

# CSRF-Konfiguration
WTF_CSRF_ENABLED = False
WTF_CSRF_COOKIE_NAME = "csrf_token"


def get_logging():
    log_file = os.path.join(LOG_DIR, 'app.log')
    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
    handler.setLevel(LOGGING_LEVEL)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOGGING_LEVEL)
    stream_handler.setFormatter(formatter)
    
    logging.basicConfig(level=LOGGING_LEVEL, handlers=[handler, stream_handler])
    
    return logging