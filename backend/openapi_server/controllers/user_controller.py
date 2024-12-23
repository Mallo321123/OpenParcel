import connexion

from openapi_server.models.security_controller_login_request import SecurityControllerLoginRequest  # noqa: E501
from openapi_server.models.user import User  # noqa: E501

from openapi_server.__init__ import get_db, close_db, get_redis
from openapi_server.tokenManager import valid_token, delete_token
from openapi_server.permission_check import check_permission

from flask_jwt_extended import jwt_required, get_jwt
from flask import request, jsonify

import jwt
import hashlib
import os
from datetime import datetime, timedelta
import re
import json


def create_user(user=None):  # noqa: E501
    db = get_db()
    cursor = db.cursor()

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user.email):
            return "Invalid email", 400
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone() is not None:
            return "User already exists", 400
        
        password_hash = hashlib.md5(user.password.encode()).hexdigest()
        cross_hash = hashlib.md5(user.username.encode() + user.password.encode()).hexdigest()
        
        user_groups_json = json.dumps(user.user_groups)
        
        cursor.execute("""INSERT INTO users (
            email, firstname, lastname, username, password_hash, cross_hash, `groups`, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (user.email, user.first_name, user.last_name, user.username, password_hash, cross_hash, user_groups_json, user.user_status))
        db.commit()
        close_db(db)
        
        return "User created", 200
        
    return "User not created", 400

def security_controller_login():  # noqa: E501
    db = get_db()
    cursor = db.cursor()
    redis_connection = get_redis()

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
        redis_connection.setex(f"jwt:{user[4]}", timedelta(hours=24), token)

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
    
    if check_permission("admin", user) is False:
        return "unauthorized", 401
    
    token = request.headers.get("Authorization").split(" ")[1]  # Token abrufen
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        return "User not found", 404
    
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db.commit()
    
    delete_token(username)
    
    return "User deleted", 200

@jwt_required()
def get_user_by_name(username):  # noqa: E501
    jwt_data = get_jwt()  # Alle Claims aus dem Token abrufen
    user = jwt_data.get("user")  # Benutzername abrufen
    token = request.headers.get("Authorization").split(" ")[1]  # Token abrufen
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    close_db(db)
    
    if user is None:
        return "User not found", 404
    
    try:
        groups = json.loads(user[7])
    except TypeError:
        groups = []
            
    user = User(
        email=user[1],
        first_name=user[2],
        last_name=user[3],
        username=user[4],
        user_groups=groups,
        user_status=user[8]
    )
    
    return jsonify(user), 200

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

@jwt_required()
def update_user(username, user=None):  # noqa: E501
    jwt_data = get_jwt()
    user = jwt_data.get("user")  # Extract username from token
    token = request.headers.get("Authorization").split(" ")[1]  # Extract token
    
    if not valid_token(user, token):
        return "unauthorized", 401
    
    if user != username and check_permission("admin", user) is False:
        return "unauthorized", 401  # Only admins and the user himself can update the user
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        return "User not found", 404
    
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
        
        if isinstance(user, User):
            user = user.to_dict()
        
        # Prepare a dictionary of fields to update
        update_fields = {}

        if user.get("email") is not None:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user['email']):
                return "Invalid email", 400
            update_fields['email'] = user['email']

        if user.get('first_name') is not None:
            update_fields['firstname'] = user['first_name']

        if user.get('last_name') is not None:
            update_fields['lastname'] = user['last_name']

        if user.get('password') is not None:
            password_hash = hashlib.md5(user['password'].encode()).hexdigest()
            cross_hash = hashlib.md5(username.encode() + user['password'].encode()).hexdigest()
            update_fields['password_hash'] = password_hash
            update_fields['cross_hash'] = cross_hash

        if user.get('user_groups') is not None:
            if check_permission("admin", user) is False:
                return "unauthorized", 401     # Only admins can change user groups
            
            user_groups_json = json.dumps(user['user_groups'])
            update_fields['`groups`'] = user_groups_json

        if user.get('user_status') is not None:
            if check_permission("admin", user) is False:
                return "unauthorized", 401      # Only admins can change user status
            
            update_fields['status'] = user['user_status']
        
        if user.get("username") is not None:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone() is not None:
                return "Username already taken", 400    # Username already taken
            
            update_fields['username'] = user['username']

        if not update_fields is not None:
            return "No fields to update", 400

        # Construct the SQL update statement dynamically
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(username)

        update_query = f"UPDATE users SET {set_clause} WHERE username = %s"

        try:
            cursor.execute(update_query, tuple(values))
            db.commit()
        except Exception as e:
            db.rollback()
            return f"Failed to update user: {e}", 500
        finally:
            close_db(db)

        return "User updated", 204
        
        
    return "Invalid request", 400 

@jwt_required()
def user_list_get():  # noqa: E501
    
    jwt_data = get_jwt()  # Alle Claims aus dem Token abrufen
    user = jwt_data.get("user")  # Benutzername abrufen
    
    if check_permission("admin", user) is False:
        return "unauthorized", 401
    
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
        try:
            groups = json.loads(users[i][7])
        except TypeError:
            groups = []
            
        users[i] = User(
            email=users[i][1],
            first_name=users[i][2],
            last_name=users[i][3],
            username=users[i][4],
            user_groups=groups,
            user_status=users[i][8]
        )
    return jsonify(users), 200
