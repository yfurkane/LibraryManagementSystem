from enum import Enum
import sqlite3 as sql

class BookState:
    Reserved = 1
    Occupied = 2
    Free = 3

class Book:

    def __init__(self, physicalAddress, title, author ): # Constructor function  
        #m_UniqueId = GenerateUniqueId()
        self.m_PhysicalAddress = physicalAddress
        self.m_Title = title
        self.m_Author = author
        self.m_State = BookState.Free
        self.m_OccupiedOrReservedBy = None
    
    
    

    # Member Functions 
    def MoveBook(self,newPhysicalAddress):
        self.m_PhysicalAddress = newPhysicalAddress
    
    def ChangeState(self,newState):
        self.m_State = newState

    # Might user be reader
    def ReserveBook(self,user):
        self.ChangeState(BookState.Reserved)
        self.m_OccupiedOrReservedBy = user

    def OccupyBook(self,user):
        self.ChangeState(BookState.Occupied)
        self.m_OccupiedOrReservedBy = user

    def FreeBook(self):
        self.ChangeState(BookState.Free)
        self.m_OccupiedOrReservedBy = None
   

    # Member Field
    m_UniqiueId = 0
    m_PhysicalAddress = {
        corridor: "",
        shelf: "",
        line: 0 
    }

    m_Title = ""
    m_Author = ""
    m_SubjectCategory = ""
    m_PublicationDate = ""
    m_State = BookState.Reserved
    m_OccupiedOrReservedBy = 1

class User:
    def __init__(self, fullName, userId, phoneNumber ):
        self.m_FullName = fullName
        self.m_UserId = userId
        self.m_PhoneNumber = phoneNumber
    
    def SearchBooks(self):
        
        while True:
            selection = input("Search By Their 1. Title 2. Author 3. Subject Category 4. Publication Date: ")
            if selection == "1":
                selection = input("Enter Title: ")
                DatabaseHandler().SearchBook(criteria = "Name", keyword = selection )
                pass
            elif selection == "2":
                selection = input("Enter Author: ")
                DatabaseHandler().SearchBook(criteria = "Author", keyword = selection )
                pass
            elif selection == "3":
                selection = input("Enter Category: ")
                DatabaseHandler().SearchBook(criteria = "Category_ID", keyword = selection )
                pass
            elif selection == "4":
                selection = input("Enter Publication Date: ")
                DatabaseHandler().SearchBook(criteria = "PublicationDate", keyword = selection )
                pass
            elif selection == ":q":
                exit()
            else:
                print("Wrong selection!")
        pass


class Reader:
    #Constructor
    def __init__(self, fullName, userId, phoneNumber,numberOfBooksOccupied):
        self.m_ReservedBooks = []
        self.m_OccupiedBooks = []
        self.m_NumberOfBooksOccupied = numberOfBooksOccupied
        User.__init__(self, fullName, userId, phoneNumber)

    def ReserveBook(self,book):
        self.m_ReservedBooks.append(book)
        self.m_NumberOfBooksOccupied += 1
        self.UpdateDatabase()

    def FreeBook(self,book):
        self.m_ReservedBooks.append(book)
        self.m_NumberOfBooksOccupied -= 1
        self.UpdateDatabase()

    def OccupyBook(self,book):
        self.m_OccupiedBooks.append(book)
        self.m_NumberOfBooksOccupied += 1
        self.UpdateDatabase()

    def UpdateDatabase(self):
        DatabaseHandler().UpdateReader(self)
        pass
    #Member Functions
    #ChangePhoneNumber
    def Dialog(self):
        print("Logged as reader")
        pass




class Librarian(User):

    #Member Functions
    #ChangePhoneNumber
    #Movebook
    #Free, Occupy, Reserve Book for User
    def OccupyBookForUser(self,user,book):
        book.OccupyBook(user)

    def Dialog(self):
        print("Logged as Librarian")
        while True:
            selection = input("What do you want: 1. Reserve book for someone 2. Free book for someone 3. Occupy book for someone 4. Search Books: ")
            if selection == "1":
                if (self.ReserveBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
            elif selection == "2":
                if (self.FreeBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
                pass
            elif selection == "3":
                if (self.OccupyBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
                pass
            elif selection == "4":
                self.SearchBooks()
                pass
            elif selection == ":q":
                exit()
            else:
                print("Wrong selection!")
        
    
        
    def ReserveBook(self):
        userId = input("Please enter user id to reserve a book: ")
        response = DatabaseHandler().CheckUserId(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            if (response["data"]["role"] == "Reader"):
                user = UserFactory.CreateUser(response["data"])
            else:
                print("Librarian user cannot reserve a book")
                return
        else:
            return False

        if user.m_NumberOfBooksOccupied > 5:
            print("User cannot occupy or reserve more than 5 books!")
            return False
        
        bookUUID = input("Please enter Book id to reserve a book: ")
        response = (DatabaseHandler().CheckBook(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.FromBookData(response["data"])
        else:
            return False
        
        if not ( book.m_State is BookState.FREE):
            print("Book is already occupied by someone")
            return False
        
        book.ReserveBook(user)
        user.ReserveBook(book)
        return True

    def FreeBook(self):
        userId = input("Please enter user id to free a book: ")
        response = DatabaseHandler().CheckUserId(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            user = UserFactory.CreateUser(response["data"])
        else:
            return False

        
        bookUUID = input("Please enter Book id to free a book: ")
        response = (DatabaseHandler().CheckBook(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.FromBookData(response["data"])
        else:
            return False
        
        if (book.m_OccupiedOrReservedBy != userId):
            print("This book is not occupied or reserved by this user!")
            return False

        book.FreeBook()
        user.FreeBook(book)
        return True

    def OccupyBook(self):
        userId = input("Please enter user id to occupy a book: ")
        response = DatabaseHandler().CheckUserId(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            user = UserFactory.CreateUser(response["data"])
        else:
            return False

        if user.m_NumberOfBooksOccupied > 5:
            return False
        
        bookUUID = input("Please enter book id to occupy a book: ")
        response = (DatabaseHandler().CheckBook(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.FromBookData(response["data"])
        else:
            return False
        
        if not ( book.m_State is BookState.FREE):
            print("Book is already occupied by someone")
            return False
        
        book.OccupyBook(user)
        user.OccupyBook(book)
        
        return True

class Librarian:
    def __init__(self,name,username): #Constructor
        self.m_Name = name
        self.m_Username = username
    

    def change_user_name(self,new_username):
        self.m_Username = new_username
        print("New User Name updated too:" , new_username)
    
    def move_book(self, book, location):
        book.change_location(location)
        print("Book", book.title,"moved to",location)
    



    #Member Functions
    #ChangePhoneNumber
    #Movebook
    #Free, Occupy, Reserve Book for User
    def OccupyBookForUser(self,user,book):
        book.OccupyBook(user)


    def Dialog():
        print("What do you want: 1. Reserve book for someone 2. Free book for someone")
        input()
        #if()
        print("For who ?")
        input()
        if(DatabaseHandler.FetchData(username)):
            pass

        pass
    # Member Field
    m_LibrarianName = ""
    m_PhoneNumber = ""

class UserFactory:
    def CreateUser(userData):
        if(userData["role"] == "Reader"):
            reader = Reader(userData["userName"],userData["userId"],userData["phoneNumber"],userData["occupiedOrReservedBooks"])
            return reader
        elif(userData["role"] == "Librarian"):
            librarian = Librarian(userData["userName"],userData["userId"],userData["phoneNumber"])
            return librarian
        else:
            print(userData["role"])

class MainHandler:
    #Constructor
    def __init__(self):
        self.m_DatabaseHandler = DatabaseHandler()
        self.m_DatabaseHandler.Init(db_file = "libraryDb (2).sqlite")
        pass
    #Connect Database
    # Member Function
    def Start(self):
        print("Welcome to Library Application")
        print("To exit from application any time enter ':q'")
        while True:
            selection = input("To Log in enter 1, To Sign up enter 2 : ")
            if selection == "1":
                self.Auth()
                self.m_LoggedInUser.Dialog()              
                break
            elif selection == "2":
                self.SignUp()
                break
            elif selection == ":q":
                print("Quit")
                break
            else:
                print("Invalid entry")
                continue

    def Auth(self):
        #Check Database
        #Get User role
        #Create user
        pwCounter = 0
        idCounter = 0
        while True:
            if (idCounter > 3):
                print("Too many wrong username try!")
                MainHandler.Shutdown()
            username = input("Username: ")
            if not (self.m_DatabaseHandler.CheckUserName(username)):
                print("Invalid username! Does not find any record")
                idCounter +=1
                continue
            while True:
                if (pwCounter > 3):
                    print("Too many wrong password try!")
                    MainHandler.Shutdown()

                password = input("Password: ")
                userData = self.m_DatabaseHandler.CheckAuth(username,password)
                if (userData == None):
                    print("Invalid password try again")
                    pwCounter+=1
                    continue
                else:
                    break
            self.m_LoggedInUser = UserFactory.CreateUser(userData)
            break
    
        
    
    def Shutdown():
        print("Exiting..")
        exit()
        
    

class DatabaseHandler:
    def __init__(self, db_file):
        self.db_file = "libraryDb.sqlite"
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

    def fetch_one(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        return self.cursor.fetchone()
    
    
    # DAtabase Connect ()
    # Fetch Data ()
    # Write Data ()
    # Update Data ()
    # Delete Data
    
    # CRUD
    pass

def main():
    '''
        Book1 = Book({"T3", "2A", 3}, "KitapGüzel" , "EKMEKCI")
        Book2 = Book({"T3", "2A", 3}, "KitapGüzel" , "EKMEKCI")
        print(Book1.m_Title)
        print(Book1.m_PhysicalAddress)
        print(Book1.m_UniqueId)
        print(Book2.m_UniqueId)
        User1=UserFactory.CreateUser("Kerim", 123, "Reader")
        print(User1.m_FullName)
        '''
        mainHandler = MainHandler()
        mainHandler.Start()


    if __name__ == "__main__":
        main()

    '''
        Welcome the application ....
        Enter UserName
        Enter PW

        MainHandler.Dialog()

    '''