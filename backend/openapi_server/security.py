import re
import unicodedata

from openapi_server.tokenManager import valid_token
from openapi_server.permission_check import check_permission

from flask_jwt_extended import get_jwt_identity
from flask import request


def normalize_input(input_value: str) -> str:
    return unicodedata.normalize("NFKC", input_value)


# Check if the value contains any SQL injection keywords
def check_sql_inject_value(value: str) -> bool:
    if not isinstance(value, str):
        return False

    value = normalize_input(value)

    sql_injection_regex = re.compile(
    r"""
    [;'"--]
    |(\b(SELECT|DROP|INSERT|DELETE|UPDATE|UNION|OR|AND)\b)
    |(\b(SELECT\s.*FROM|DROP\s.*TABLE)\b)
    """,
    re.IGNORECASE | re.VERBOSE,
)


    return bool(sql_injection_regex.search(value))

def check_sql_inject_json(**kwargs: dict) -> bool:
    for key, value in kwargs.items():
        if isinstance(value, str) and check_sql_inject_value(value):
            print(f"Unsichere Eingabe erkannt: {key} = {value}")
            return True
    return False


def check_auth(group = None):
    token = request.cookies.get('access_token')
    try:
        user = get_jwt_identity()
    except Exception:
        return False
    
    if not valid_token(user, token):
        return False
    
    if group is not None:
        if not check_permission(group, user) or not check_permission("admin", user):
            return False
        
    return True