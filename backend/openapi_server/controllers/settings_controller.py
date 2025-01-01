import connexion

from flask_jwt_extended import jwt_required

from openapi_server.models.settings import Settings  # noqa: E501

from openapi_server.db import get_db, close_db

from openapi_server.security import check_sql_inject_json, check_auth

from openapi_server.config import get_logging

logging = get_logging()

@jwt_required()
def settings_list():  # noqa: E501
    if not check_auth("admin"):
        return "unauthorized", 401

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
    if not check_auth("admin"):
        return "unauthorized", 401
    
    if connexion.request.is_json:
        settings = Settings.from_dict(connexion.request.get_json())  # noqa: E501
        
        if isinstance(settings, Settings):
            settings = settings.to_dict()
            
        if check_sql_inject_json(**settings):
            return "Invalid value", 400
        
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
        
        logging.info("Settings updated")
        return "Ok", 200
    
    logging.warning("Invalid request in settings_update")
    return "invalid Request", 400
