from typing import List

import os
import jwt

def info_from_BearerAuth(token):
    """
    Check and retrieve authentication information from custom bearer token.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param token Token provided by Authorization header
    :type token: str
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """
    try:
        decoded_token = jwt.decode(token, os.getenv('SECRET_KEY', 'default'), algorithms=["HS256"])
        return {'uid': decoded_token['user']}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

