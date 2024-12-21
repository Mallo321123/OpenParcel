import connexion

from openapi_server.models.security_controller_login_request import SecurityControllerLoginRequest  # noqa: E501
from openapi_server.models.user import User  # noqa: E501

from openapi_server.__init__ import get_db, close_db, get_redis

import jwt
import hashlib
import os
from datetime import datetime, timedelta
import re

from openapi_server.tokenManager import valid_token, delete_token

from flask_jwt_extended import jwt_required, get_jwt
from flask import request, jsonify


def create_user(user=None):  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param user: Created user object
    :type user: dict | bytes

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user.email):
            return "Invalid email", 400
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone() is not None:
            return "User already exists", 400
        
        password_hash = hashlib.md5(user.password.encode()).hexdigest()
        cross_hash = hashlib.md5(user.username.encode() + user.password.encode()).hexdigest()
        
        cursor.execute("""INSERT INTO users (
            email, firstname, lastname, username, password_hash, cross_hash, `groups`, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (user.email, user.first_name, user.last_name, user.username, password_hash, cross_hash, user.user_groups, user.user_status))
        db.commit()
        close_db(db)
        
        return "User created", 200
        
    return "User not created", 400

def security_controller_login():  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    redis_connection = get_redis()
    """User Login

    Authenticates a user and returns a JWT token. # noqa: E501

    :param security_controller_login_request: 
    :type security_controller_login_request: dict | bytes

    :rtype: Union[SecurityControllerLogin200Response, Tuple[SecurityControllerLogin200Response, int], Tuple[SecurityControllerLogin200Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        login = SecurityControllerLoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
        
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (login.username,))
        user = cursor.fetchone()
        if user is None:
            return "Login or password Invalid", 401
        
        password_hash = hashlib.md5(login.password.encode()).hexdigest()
        cross_hash = hashlib.md5(login.username.encode() + login.password.encode()).hexdigest()
    
        
        if user[5] != password_hash or user[6] != cross_hash:
            return "Login or password Invalid", 401
        
        # Generate JWT token
        secret_key = os.getenv("SECRET_KEY", "default_secret")
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        token_payload = {
            "user": user[4],
            "id": user[0],
            "exp": expiration_time
        }
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")

        # Store token in Redis
        redis_connection.setex(user[4], timedelta(hours=24), token)

        return {
            "success": True,
            "message": "Login successful.",
            "token": token
        }

    close_db(db)
    return "Login or password Invalid", 401

@jwt_required()
def delete_user(username):  # noqa: E501
    
    jwt_data = get_jwt()  # Alle Claims aus dem Token abrufen
    user = jwt_data.get("user")  # Benutzername abrufen
    token = request.headers.get("Authorization").split(" ")[1]  # Token abrufen
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        return "User not found", 404
    
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db.commit()
    
    delete_token(username)
    
    return "User deleted", 200


def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing. 
    :type username: str

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    return 'do some magic!'

@jwt_required()
def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    jwt_data = get_jwt()  # Alle Claims aus dem Token abrufen
    user = jwt_data.get("user")  # Benutzername abrufen
    delete_token(user)
    
    return "User logged out", 200



def update_user(username, user=None):  # noqa: E501
    """Update user

    This can only be done by the logged in user. # noqa: E501

    :param username: name of user that needs to be changed
    :type username: str
    :param user: Update an existent user in the store
    :type user: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

@jwt_required()
def user_list_get():  # noqa: E501
    
    jwt_data = get_jwt()  # Alle Claims aus dem Token abrufen
    user = jwt_data.get("user")  # Benutzername abrufen
    token = request.headers.get("Authorization").split(" ")[1]  # Token abrufen
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()
    """list users

    list all users # noqa: E501


    :rtype: Union[List[User], Tuple[List[User], int], Tuple[List[User], int, Dict[str, str]]
    """
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    close_db(db)
    
    for i in range(len(users)):
        users[i] = User(
            email=users[i][1],
            first_name=users[i][2],
            last_name=users[i][3],
            username=users[i][4],
            user_groups=users[i][7],
            user_status=users[i][8]
        )
    return jsonify(users), 200
