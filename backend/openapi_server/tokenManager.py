from openapi_server.db import get_redis, close_redis
from jwt import ExpiredSignatureError, InvalidTokenError

from openapi_server.config import get_logging

logging = get_logging()

def valid_token(username, token):
    redis_connection = get_redis()
    
    try:
        # Retrieve the token from Redis
        redis_token = redis_connection.get(f"jwt:{username}")

        if redis_token is None:
            logging.error(f"Token not found for user {username}.")
            return False

        # Compare tokens
        if redis_token != token:
            logging.error(f"Token mismatch for user {username}.")
            return False

        return True

    except ExpiredSignatureError:
        logging.error(f"Expired token user: {username}.")
        return False

    except InvalidTokenError:
        logging.error(f"Invalid token user: {username}.")
        return False
    
    finally:
        close_redis(redis_connection)
    
def delete_token(username):
    redis_connection = get_redis()
    redis_connection.delete(f"jwt:{username}")
    logging.info(f"Token deleted for user {username}.")
    close_redis(redis_connection)