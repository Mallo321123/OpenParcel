import connexion

from flask_jwt_extended import jwt_required, get_jwt
from flask import request

from openapi_server.models.settings import Settings  # noqa: E501

from openapi_server.__init__ import get_db, close_db
from openapi_server.tokenManager import valid_token
from openapi_server.permission_check import check_permission

@jwt_required()
def settings_list():  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")  # Extract username from token
    token = request.headers.get("Authorization").split(" ")[1]  # Extract token

    if not valid_token(user, token):
        return "unauthorized", 401
    
    if check_permission("admin", user) is False:
        return "unauthorized", 401     # Only admins can change settings

    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT value FROM settings WHERE name = 'min_password_length'")
    min_password_length = cursor.fetchone()
    close_db(db)
    
    response = {
        "minPasswordLength": int(min_password_length[0])
    }
    
    return response, 200

@jwt_required()
def settings_update():  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")  # Extract username from token
    token = request.headers.get("Authorization").split(" ")[1]  # Extract token

    if not valid_token(user, token):
        return "unauthorized", 401
    
    if check_permission("admin", user) is False:
        return "unauthorized", 401     # Only admins can change settings
    
    if connexion.request.is_json:
        settings = Settings.from_dict(connexion.request.get_json())  # noqa: E501
        
        if isinstance(settings, Settings):
            settings = settings.to_dict()
        
        db = get_db()
        cursor = db.cursor()
        
        if settings.get('min_password_length') is not None:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'min_password_length'", (settings.get('min_password_length'),))
        
        db.commit()
        close_db(db)
        return "Ok", 200
    return 400
