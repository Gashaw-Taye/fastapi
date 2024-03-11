# database.py

import mysql.connector

def create_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "testdb",
    }

    # Create a connection pool
    db_conn = mysql.connector.connect(pool_name="student_pool", pool_size=10, **db_config)

    return db_conn

def create_cursor(connection):
    # Create a cursor object
    return connection.cursor(dictionary=True)
