import re


# Check if the value contains any SQL injection keywords
def check_sql_inject_value(value: str) -> bool:
    
    
    SQL_INJECTION_REGEX = re.compile(
        r"[;'\"--]|(\b(SELECT|DROP|INSERT|DELETE|UPDATE|UNION|OR|AND)\b)", re.IGNORECASE
    )
    
    if value is not None and SQL_INJECTION_REGEX.search(value):
        return False
    else:
        return True

def check_sql_inject_json(**kwargs) -> bool:
    
    for key, value in kwargs.items():
        if not check_sql_inject_value(value):
            print(f"Unsichere Eingabe erkannt: {key} = {value}")
            return False
    return True