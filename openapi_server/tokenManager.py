from openapi_server.__init__ import get_redis
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
import os


def valid_token(username, token):
    redis_connection = get_redis()
    
    try:
        # Retrieve the token from Redis
        redis_token = redis_connection.get(f"jwt:{username}")

        if redis_token is None:
            print("Token not found in Redis.")
            return False

        # Compare tokens
        if redis_token != token:
            print("Token mismatch.")
            return False

        return True

    except ExpiredSignatureError:
        print("Token has expired.")
        return False

    except InvalidTokenError:
        print("Invalid token.")
        return False
    
def delete_token(username):
    redis_connection = get_redis()
    redis_connection.delete(f"jwt:{username}")