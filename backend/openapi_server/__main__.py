#!/usr/bin/env python3

import connexion
import os

from openapi_server import encoder
from openapi_server.db import prepare_database
from flask_jwt_extended import JWTManager

from flask.json.provider import DefaultJSONProvider

from flask_cors import CORS  # Importiere CORS


app = connexion.App(__name__, specification_dir='./openapi/')
    
flask_app = app.app

CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

flask_app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
flask_app.config["JWT_IDENTITY_CLAIM"] = "user"
jwt = JWTManager(flask_app)
    
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'OpenParcel'},
            pythonic_params=True)
    
prepare_database()

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT', '8080'))