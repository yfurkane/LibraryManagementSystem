from database import DatabaseHandler
from Book import *

class User:
    def __init__(self, fullName, userId, phoneNumber ):
        self.m_FullName = fullName
        self.m_UserId = userId
        self.m_PhoneNumber = phoneNumber
    
    def searchBooks(self):
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

    def reserveBook(self):
        if self.m_NumberOfBooksOccupied > 5:
            print("User cannot occupy or reserve more than 5 books!")
            return False
        
        bookUUID = input("Please enter Book id to reserve a book: ")
        response = (DatabaseHandler().CheckBook(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.fromBookData(response["data"])
        else:
            return False
        
        if not ( book.m_State is BookState.FREE):
            print("Book is already occupied by someone")
            return False
        
        book.ReserveBook(self)

        self.m_ReservedBooks.append(book)
        self.m_NumberOfBooksOccupied += 1
        self.updateDatabase()
        return True

    def freeBook(self):
        
        bookUUID = input("Please enter Book id to free a book: ")
        response = (DatabaseHandler().check_book(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.fromBookData(response["data"])
        else:
            return False
        
        if (int(book.m_OccupiedOrReservedBy) != self.m_UserId):
            print("This book is not occupied or reserved by this user! ", book.m_OccupiedOrReservedBy)
            return False

        book.FreeBook()

        self.m_ReservedBooks.append(book)
        self.m_NumberOfBooksOccupied -= 1
        self.updateDatabase()

        return True

    def occupyBook(self):

        if self.m_NumberOfBooksOccupied > 5:
            return False
        
        bookUUID = input("Please enter book id to occupy a book: ")
        response = (DatabaseHandler().check_book(bookUUID)) # If response is none there is no existing book with this id

        if(response["result"] is not False):
            book = Book.fromBookData(response["data"])
        else:
            return False
        
        if not ( book.m_State is BookState.FREE):
            print("Book is already occupied by someone")
            return False
        
        book.occupyBook(self)

        self.m_OccupiedBooks.append(book)
        self.m_NumberOfBooksOccupied += 1
        self.updateDatabase()
        return True

    def updateDatabase(self):
        DatabaseHandler().update_reader(self)
        pass
    #Member Functions
    def dialog(self):
        print(f"{self.m_FullName} Logged as Reader")
        while True:
            selection = input("What do you want: 1. Reserve book for yourself 2. Free book for yourself 3. Occupy book for yourself 4. Search Books: ")
            if selection == "1":
                if (self.reserveBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
            elif selection == "2":
                if (self.freeBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                
            elif selection == "3":
                if (self.occupyBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                
                
            elif selection == "4":
                self.searchBooks()
                
            elif selection == ":q":
                exit()
            else:
                print("Wrong selection!")
        pass




class Librarian(User):

    #Member Functions
    #ChangePhoneNumber
    #Movebook
    #Free, Occupy, Reserve Book for User
    def occupyBookForUser(self,user,book):
        book.occupyBook(user)

    def dialog(self):
        print(f"{self.m_FullName} Logged as Librarian")
        while True:
            selection = input("What do you want: 1. Reserve book for someone 2. Free book for someone 3. Occupy book for someone 4. Search Books: ")
            if selection == "1":
                if (self.reserveBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
            elif selection == "2":
                if (self.freeBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
                pass
            elif selection == "3":
                if (self.occupyBook()):
                    print("Operation success")
                else:
                    print("Operation Failed")
                pass
                pass
            elif selection == "4":
                self.searchBooks()
                pass
            elif selection == ":q":
                exit()
            else:
                print("Wrong selection!")
        
    
        
    def reserveBook(self):
        userId = input("Please enter user id to reserve a book: ")
        response = DatabaseHandler().check_user_Id(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            if (response["data"]["role"] == "Reader"):
                user = UserFactory.createUserreateUser(response["data"])
            else:
                print("Librarian user cannot reserve a book")
                return
        else:
            return False

        
        return user.reserveBook()
     

    def freeBook(self):
        userId = input("Please enter user id to free a book: ")
        response = DatabaseHandler().check_user_Id(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            user = UserFactory.createUser(response["data"])
        else:
            return False

        return user.freeBook()

    def occupyBook(self):
        userId = input("Please enter user id to occupy a book: ")
        response = DatabaseHandler().check_user_Id(userId) # If response is none there is no existing user with this id 
        if(response["result"] is not False):
            user = UserFactory.createUser(response["data"])
        else:
            return False


        return user.occupyBook()
        

class UserFactory:
    def createUser(userData):
        if(userData["role"] == "Reader"):
            reader = Reader(userData["userName"],userData["userId"],userData["phoneNumber"],userData["occupiedOrReservedBooks"])
            return reader
        elif(userData["role"] == "Librarian"):
            librarian = Librarian(userData["userName"],userData["userId"],userData["phoneNumber"])
            return librarian
        else:
            print(userData["role"])
