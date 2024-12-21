#!/usr/bin/env python3

import connexion
import os

from openapi_server import encoder
from openapi_server.__init__ import prepare_database
from flask_jwt_extended import JWTManager



app = connexion.App(__name__, specification_dir='./openapi/')
    
flask_app = app.app
jwt = JWTManager(flask_app)
    
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'OpenParcel'},
            pythonic_params=True)
    
prepare_database()

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT', '8080'))