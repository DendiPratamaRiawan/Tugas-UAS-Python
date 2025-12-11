import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_gadget"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def fetch(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
