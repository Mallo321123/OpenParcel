import mysql.connector
import os
import time
import redis

from mysql.connector import Error

# Create Database connection
def get_db():
    retries = 5
    while retries > 0:
        try:
            db = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                port=int(os.getenv('MYSQL_PORT', '3306')),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'example'),
                database=os.getenv('MYSQL_DATABASE', 'OpenParcel')
            )
            break
        except Error as e:
            print(f"Verbindung fehlgeschlagen: {e}, neuer Versuch in 5 Sekunden...")
            retries -= 1
            time.sleep(5)
    if not db:
        raise ConnectionError("MySQL-Datenbank konnte nach mehreren Versuchen nicht erreicht werden.")
    return db

# Close Database connection
def close_db(db):
    if db is not None:
        db.close()
    return True

def get_redis():
    try:
        redis_connection = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'redis'), port=os.getenv('REDIS_PORT', '6379'), decode_responses=True)

    except redis.ConnectionError:
        print("Redis connection error.")
        return None
    return redis_connection

def close_redis(redis_connection):
    if redis_connection is not None:
        redis_connection.close()
    return True

def settings_default():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM settings")
    result = cursor.fetchone()
    
    if result is None:
        cursor.execute("INSERT INTO settings (name, value) VALUES ('min_password_length', '5')")
        db.commit()


def prepare_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS OpenParcel")
    cursor.execute("USE OpenParcel")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        value TEXT
        )""")
    
    settings_default()  # Only sets settings, if database is empty
    
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
        addDate DATE,
        closeDate DATE DEFAULT NULL,
        products VARCHAR(255),
        notes TEXT DEFAULT NULL,
        state VARCHAR(255)
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
    db.commit()
    close_db(db)