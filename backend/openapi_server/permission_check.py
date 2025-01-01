from openapi_server.db import get_db, close_db
import json

from openapi_server.config import get_logging

logging = get_logging()

def check_permission(permission: str, username: str) -> bool:
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT `groups` FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
            
        if not result or not result[0]:
            logging.warning(f"User {username} not found or has no groups.")
            return False
        
        try:
            groups = json.loads(result[0])
        except json.JSONDecodeError:
            logging.error(f"Error decoding groups for user {username}.")
            return False

        close_db(db)
        return permission in groups

    except Exception as e:
        logging.error(f"Fehler bei der Berechtigungsprüfung von {username}: {e}")
        close_db(db)
        return False
    