import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.security_controller_login200_response import SecurityControllerLogin200Response  # noqa: E501
from openapi_server.models.security_controller_login_request import SecurityControllerLoginRequest  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server import util

from openapi_server.__init__ import get_db, close_db, get_redis

import jwt
import hashlib
import os
from datetime import datetime, timedelta
import redis

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


def delete_user(username):  # noqa: E501
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
    
    return "User deleted", 200


def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing. 
    :type username: str

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def security_controller_login(security_controller_login_request):  # noqa: E501
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
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        token_payload = {
            "user": user['username'],
            "uid": user['id'],
            "exp": expiration_time
        }
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")

        # Store token in Redis
        redis_connection.setex(f"jwt:{user['id']}", timedelta(hours=1), token)

        return {
            "success": True,
            "message": "Login successful.",
            "token": token
        }

    return 'do some magic!'


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


def user_list_get():  # noqa: E501
    """list users

    list all users # noqa: E501


    :rtype: Union[List[User], Tuple[List[User], int], Tuple[List[User], int, Dict[str, str]]
    """
    return 'do some magic!'
