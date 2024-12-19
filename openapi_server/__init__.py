import mysql.connector
import os
import time

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

def prepare_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS OpenParcel")
    cursor.execute("USE OpenParcel")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        username VARCHAR(255),
        password_hash VARCHAR(255),
        cross_hash VARCHAR(255),
        `groups` VARCHAR(255),
        status INT
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer VARCHAR(255),
        addDate DATE,
        closeDate DATE,
        products VARCHAR(255),
        state VARCHAR(255)
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        comment TEXT,
        customerGroups VARCHAR(255),
        difficulty INT,
        buildTime VARCHAR(255)
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS lights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        adress VARCHAR(255),
        `groups` VARCHAR(255),
        comment TEXT
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `group` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS mapper (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name TEXT,
        lights VARCHAR(255),
        products VARCHAR(255)
        )""")
    db.commit()
    close_db(db)