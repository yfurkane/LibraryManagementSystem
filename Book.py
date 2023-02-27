from database import DatabaseHandler
from bookState import BookState
import uuid

class Util:
    def generateuniqueId():
        return uuid.uuid4()

class Book:
    def __init__(self, physicalAddress, title, author,publicationDate, bookState = BookState.FREE, occupiedOrReservedBy = None, UUID = None ): # Constructor function  
        self.m_PhysicalAddress = physicalAddress
        self.m_Title = title
        self.m_Author = author
        self.m_State = bookState
        self.m_PublicationDate = publicationDate
        self.m_OccupiedOrReservedBy = occupiedOrReservedBy

        if (UUID is not None):
            self.m_UniqueId = UUID
        else:
            self.m_UniqueId = Util.GenerateUniqueId()

    @classmethod
    def fromBookData(cls, bookData):
        state = BookState.FREE

        if(bookData["bookState"] == "Occupied"):
            state = BookState.OCCUPIED
        elif(bookData["bookState"]=="Reserved"):
            state = BookState.RESERVED

        return cls(bookData["physicalAddress"],bookData["title"],bookData["author"],
                    bookData["publicationDate"],state,bookData["occupiedOrReservedBy"],bookData["UUID"])

    # Member Functions 
    def moveBook(self,newPhysicalAddress):
        self.m_PhysicalAddress = newPhysicalAddress
    
    def changeState(self,newState):
        self.m_State = newState

    # Might user be reader
    def reserveBook(self,user):
        self.changeState(BookState.RESERVED)
        self.m_OccupiedOrReservedBy = user
        self.updateDatabase()

    def occupyBook(self,user):
        self.changeState(BookState.OCCUPIED)
        self.m_OccupiedOrReservedBy = user
        self.updateDatabase()

    def freeBook(self):
        self.changeState(BookState.FREE)
        self.m_OccupiedOrReservedBy = None
        self.updateDatabase()
    
    def updateDatabase(self):
        # Database Query
        DatabaseHandler().update_book(self)
        pass


