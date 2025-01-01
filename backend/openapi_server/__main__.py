#!/usr/bin/env python3

import connexion
import os
from openapi_server import encoder
from openapi_server.db import prepare_database
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from openapi_server.config import (
    csrf,
    SECRET_KEY,
    JWT_SECRET_KEY,
    JWT_IDENTITY_CLAIM,
    JWT_TOKEN_LOCATION,
    JWT_ACCESS_COOKIE_NAME,
    WTF_CSRF_ENABLED,
    WTF_CSRF_COOKIE_NAME,
)

# Flask- und Connexion-Initialisierung
app = connexion.App(__name__, specification_dir="./openapi/")
flask_app = app.app

# CORS aktivieren
CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

# Flask-Konfiguration aus config.py
flask_app.config["SECRET_KEY"] = SECRET_KEY
flask_app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
flask_app.config["JWT_IDENTITY_CLAIM"] = JWT_IDENTITY_CLAIM
flask_app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
flask_app.config["JWT_ACCESS_COOKIE_NAME"] = JWT_ACCESS_COOKIE_NAME

# CSRF und WTF-CSRF-Einstellungen
flask_app.config["WTF_CSRF_ENABLED"] = WTF_CSRF_ENABLED
flask_app.config["WTF_CSRF_COOKIE_NAME"] = WTF_CSRF_COOKIE_NAME

# CSRF und JWT
csrf.init_app(flask_app)
jwt = JWTManager(flask_app)

# JSON Encoder und API hinzufügen
app.app.json_encoder = encoder.JSONEncoder
app.add_api("openapi.yaml", arguments={"title": "OpenParcel"}, pythonic_params=True)

prepare_database()

if __name__ == "__main__":
    app.run(port=os.getenv("FLASK_PORT", "8080"))
