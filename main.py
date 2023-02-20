from enum import Enum
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


class Reader:
    #Constructor
    def __init__(self) -> None:
        pass

    #Member Functions
    #ChangePhoneNumber
    def Dialog():
        pass

    # Member Field
    m_ReaderName = ""
    m_LibraryId = ""
    m_PhoneNumber = ""
    m_NumberOfBooksOccupied = 0
    m_ReservedBooks = []
    m_OccupiedBooks = []

class Librarian:
    #Constructor

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
    def CreateUser(username,phonenumber,role):
        if(role == "Reader"):
            return Reader(username)
        elif(role=="Librarian"):
            return Librarian(user)

class MainHandler:
    #Constructor
    #Connect Database
    # Member Function
    def Auth(self, username,pw):
        #Check Database
        #Get User role
        #Create user
        self.m_User = CreateUser(username,phonenumber,role) 
    
    def Dialog():
        m_User.Dialog()
    
    
    m_User = None

class DatabaseHandler:
    # DAtabase Connect ()
    # Fetch Data ()
    # Write Data ()
    # Update Data ()
    # Delete Data
    
    # CRUD
    pass

def main():
    Book1 = Book({"T3", "2A", 3}, "KitapGüzel" , "EKMEKCI")

'''
    Welcome the application ....
    Enter UserName
    Enter PW

    MainHandler.Dialog()

'''