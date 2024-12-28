from openapi_server.db import get_db, close_db
import json

def check_permission(permission: str, username: str) -> bool:
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT `groups` FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if not result or not result[0]:
                return False
            
            # Parse JSON und prüfen
            try:
                groups = json.loads(result[0])
            except json.JSONDecodeError:
                return False

            close_db(db)
            return permission in groups

    except Exception as e:
        # Logge den Fehler (falls ein Logging-System vorhanden ist)
        print(f"Fehler bei der Berechtigungsprüfung: {e}")
        close_db(db)
        return False