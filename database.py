import sqlite3 as sql
import libraryDb.sqlite
db_file = libraryDb.sqlite

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def execute(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connection.commit()

    def fetch_all(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        return self.cursor.fetchall()