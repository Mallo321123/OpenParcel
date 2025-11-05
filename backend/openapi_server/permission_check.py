from openapi_server.db import get_db, close_db
import json
import time

from openapi_server.config import get_logging

logging = get_logging()

# Cache for user permissions to reduce database queries
_permissions_cache = {}
_permissions_cache_time = {}
PERMISSIONS_CACHE_TTL = 300  # 5 minutes

def check_permission(permission: str, username: str) -> bool:
    try:
        current_time = time.time()
        cache_key = f"{username}:permissions"
        
        # Check cache validity
        if cache_key in _permissions_cache:
            if current_time - _permissions_cache_time.get(cache_key, 0) < PERMISSIONS_CACHE_TTL:
                groups = _permissions_cache[cache_key]
                return permission in groups
        
        # Fetch from database if cache miss or expired
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT `groups` FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
            
        if not result or not result[0]:
            close_db(db)
            logging.warning(f"User {username} not found or has no groups.")
            return False
        
        try:
            groups = json.loads(result[0])
        except json.JSONDecodeError:
            close_db(db)
            logging.error(f"Error decoding groups for user {username}.")
            return False

        close_db(db)
        
        # Update cache
        _permissions_cache[cache_key] = groups
        _permissions_cache_time[cache_key] = current_time
        
        return permission in groups

    except Exception as e:
        logging.error("Error during permission check")
        return False
    