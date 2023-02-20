import sqlite3 as sql

db_file = "libraryDb.sqlite"

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

class reader:
    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS Members(
                    MemberID Integer Primary Key AUTOINCREMENT,
                    FirstName Text,
                    LastName Text,
                    Type Text,
                    Mail Text,
                    Password Text,
                    TookedBooks Integer)"""
    
    def categories(self):
        sql = """ CREATE TABLE IF NOT EXISTS Categories(
                    CategoryID Integer Primary KEy AUTOINCREMENT,
                    Name Text )"""
    def books(self):
        sql =  """ CREATE TABLE IF NOT EXISTS Books(
                    BookID Integer Primary Key AUTOINCREMENT,
                    Name Text,
                    Author Text,
                    ISBN Integer,
                    Address Text,
                    PublicationDate Text,
                    Status Text,
                    Category_ID Integer,
                    Foreign Key(Category_ID) References Categories(CategoryID))
                    """
    def occupied_books(self):
        sql= """ CREATE TABLE IF NOT EXISTS TookBooks(
                    TookBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer ,
                    BookID Integer,
                    TookDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))"""
        
    
    def reserved_books(self):
        sql = """ CREATE TABLE IF NOT EXISTS ReceivedBooks(
                    ReceivedBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer,
                    BookID Integer ,
                    ReceivedDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))"""
    
    def free_books(self):
        sql = """ CREATE TABLE IF NOT EXISTS ReturnedBooks(
                    ReturnedBookID Integer Primary Key AUTOINCREMENT,
                    MemberID Integer,
                    BookID Integer,
                    ReturnedDate Text,
                    Foreign Key(MemberID) references Members(MemberID),
                    Foreign Key(BookID) references Books(BookID))"""
                
