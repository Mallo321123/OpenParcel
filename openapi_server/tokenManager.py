from openapi_server.__init__ import get_redis
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
import os


def valid_token(username, token):
    redis_connection = get_redis()
    
    try:
        # Retrieve the token from Redis
        redis_token = redis_connection.get(username)

        if redis_token is None:
            print("Token not found in Redis.")
            return None

        # Compare tokens
        if redis_token != token:
            print("Token mismatch.")
            return None

        # Decode the token
        decoded_token = jwt.decode(
            token,
            os.getenv("SECRET_KEY", "default_secret"),
            algorithms=["HS256"]
        )

        return decoded_token

    except ExpiredSignatureError:
        print("Token has expired.")
        return None

    except InvalidTokenError:
        print("Invalid token.")
        return None