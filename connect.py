import mysql.connector

def get_database_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="court"
        )
        return db
    except mysql.connector.Error as err:
        print("Error:", err)

def get_database_cursor(db):
    try:
        cursor = db.cursor()
        return cursor
    except mysql.connector.Error as err:
        print("Error:", err)
