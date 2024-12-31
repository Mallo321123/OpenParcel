import connexion

from flask_jwt_extended import jwt_required, get_jwt
from flask import request

from openapi_server.models.settings import Settings  # noqa: E501

from openapi_server.db import get_db, close_db
from openapi_server.tokenManager import valid_token
from openapi_server.permission_check import check_permission

from openapi_server.security import check_sql_inject_json

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
    
    cursor.execute("SELECT value FROM settings WHERE name = 'blockTime'")
    block_time = cursor.fetchone()
    
    cursor.execute("SELECT value FROM settings WHERE name = 'maxLoginAttempts'")
    max_login_attempts = cursor.fetchone()
    
    cursor.execute("SELECT value FROM settings WHERE name = 'tokenExpire'")
    token_expire = cursor.fetchone()
    close_db(db)
    
    response = {
        "minPasswordLength": int(min_password_length[0]),
        "blockTime": int(block_time[0]),
        "maxLoginAttempts": int(max_login_attempts[0]),
        "tokenExpire": int(token_expire[0])
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
        
        if check_sql_inject_json(settings):
            return "Invalid value", 400
        
        if isinstance(settings, Settings):
            settings = settings.to_dict()
        
        db = get_db()
        cursor = db.cursor()
        
        if settings.get('min_password_length') is not None:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'min_password_length'", (settings.get('min_password_length'),))
            
        if settings.get('block_time') is not None:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'blockTime'", (settings.get('block_time'),))
            
        if settings.get('max_login_attempts') is not None:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'maxLoginAttempts'", (settings.get('max_login_attempts'),))
        
        if settings.get('token_expire') is not None:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'tokenExpire'", (settings.get('token_expire'),))
        
        db.commit()
        close_db(db)
        return "Ok", 200
    return "invalid Request", 400
