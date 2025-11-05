import mysql.connector
from mysql.connector import pooling, Error
import os
import time
import redis
import threading

from openapi_server.config import get_logging

logging = get_logging()

# Connection pool for MySQL
_db_pool = None
_redis_pool = None

def _init_db_pool():
    """Initialize the database connection pool"""
    global _db_pool
    if _db_pool is None:
        retries = 5
        while retries > 0:
            try:
                _db_pool = pooling.MySQLConnectionPool(
                    pool_name="openparcel_pool",
                    pool_size=10,
                    pool_reset_session=True,
                    host=os.getenv('MYSQL_HOST', 'mysql'),
                    port=int(os.getenv('MYSQL_PORT', '3306')),
                    user=os.getenv('MYSQL_USER', 'root'),
                    password=os.getenv('MYSQL_PASSWORD', 'example'),
                    database=os.getenv('MYSQL_DATABASE', 'OpenParcel')
                )
                logging.info("Database connection pool initialized successfully")
                break
            except Error as e:
                logging.warning("Database pool initialization failed, retrying in 5 seconds...")
                retries -= 1
                time.sleep(5)
        if _db_pool is None:
            logging.error("Database pool could not be initialized after multiple attempts")
            raise ConnectionError("Database pool could not be initialized after multiple attempts")
    return _db_pool

# Create Database connection from pool
def get_db():
    pool = _init_db_pool()
    try:
        return pool.get_connection()
    except Error as e:
        logging.error("Failed to get database connection from pool")
        raise

# Close Database connection (returns to pool)
def close_db(db):
    if db is not None:
        db.close()
    return True

def _init_redis_pool():
    """Initialize Redis connection pool"""
    global _redis_pool
    if _redis_pool is None:
        try:
            _redis_pool = redis.ConnectionPool(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', '6379')),
                decode_responses=True,
                max_connections=10
            )
            logging.info("Redis connection pool initialized successfully")
        except redis.ConnectionError:
            logging.error("Redis connection pool initialization error")
            return None
    return _redis_pool

def get_redis():
    pool = _init_redis_pool()
    if pool is None:
        return None
    try:
        return redis.StrictRedis(connection_pool=pool)
    except redis.ConnectionError:
        logging.error("Redis connection error.")
        return None

def close_redis(redis_connection):
    if redis_connection is not None:
        redis_connection.close()
    return True

# Settings cache to avoid repeated queries
_settings_cache = {}
_settings_cache_time = 0
_settings_cache_lock = threading.Lock()
SETTINGS_CACHE_TTL = 300  # 5 minutes

def get_setting(setting_name):
    """Get a setting value with caching"""
    global _settings_cache, _settings_cache_time
    
    current_time = time.time()
    # Check if cache is valid (thread-safe)
    with _settings_cache_lock:
        if current_time - _settings_cache_time > SETTINGS_CACHE_TTL:
            _settings_cache = {}
            _settings_cache_time = current_time
        
        # Return from cache if available
        if setting_name in _settings_cache:
            return _settings_cache[setting_name]
    
    # Fetch from database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT value FROM settings WHERE name = %s", (setting_name,))
    result = cursor.fetchone()
    close_db(db)
    
    if result:
        value = result[0]
        with _settings_cache_lock:
            _settings_cache[setting_name] = value
        return value
    return None

def settings_default():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM settings")
    result = cursor.fetchone()
    
    if result is None:
        cursor.execute("INSERT INTO settings (name, value) VALUES ('min_password_length', '5')")
        cursor.execute("INSERT INTO settings (name, value) VALUES ('blockTime', '600')")
        cursor.execute("INSERT INTO settings (name, value) VALUES ('maxLoginAttempts', '5')")
        cursor.execute("INSERT INTO settings (name, value) VALUES ('tokenExpire', '24')")
        logging.info("Settings default values set.")
        db.commit()


def prepare_database():
    logging.info("Preparing database...")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS OpenParcel")
    cursor.execute("USE OpenParcel")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        value TEXT
        )""")
    
    settings_default()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) DEFAULT NULL,
        firstname VARCHAR(255) DEFAULT NULL,
        lastname VARCHAR(255) DEFAULT NULL,
        username VARCHAR(255),
        password_hash VARCHAR(255),
        cross_hash VARCHAR(255),
        `groups` VARCHAR(255) DEFAULT NULL,
        status INT DEFAULT 0
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer VARCHAR(255),
        addDate DATETIME,
        closeDate DATETIME DEFAULT NULL,
        products TEXT,
        comment TEXT DEFAULT NULL,
        state VARCHAR(255),
        shipmentType VARCHAR(255)
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        comment TEXT DEFAULT NULL,
        customerGroups VARCHAR(255) DEFAULT NULL,
        difficulty INT DEFAULT NULL,
        buildTime VARCHAR(255) DEFAULT NULL
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS lights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        adress VARCHAR(255) DEFAULT NULL,
        `groups` VARCHAR(255) DEFAULT NULL,
        comment TEXT DEFAULT NULL
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `group` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS mapper (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name TEXT,
        lights VARCHAR(255) DEFAULT NULL,
        products VARCHAR(255) DEFAULT NULL
        )""")
    
    # Create indexes for frequently queried columns
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_settings_name ON settings(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_state ON orders(state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_shipmentType ON orders(shipmentType)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_difficulty ON products(difficulty)")
    logging.info("Database indexes created successfully")
    
    db.commit()
    close_db(db)
    logging.info("Preparings Database ... done")