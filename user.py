from database import DatabaseHandler
from Book import *

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


class Reader(User):
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
