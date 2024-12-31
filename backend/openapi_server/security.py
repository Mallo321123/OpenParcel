import re
import unicodedata


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
