from database import DatabaseHandler
from BookState import BookState
class Util:
    def GenerateUniqueId():
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
    def FromBookData(cls, bookData):
        state = BookState.FREE

        if(bookData["bookState"] == "Occupied"):
            state = BookState.OCCUPIED
        elif(bookData["bookState"]=="Reserved"):
            state = BookState.RESERVED

        return cls(bookData["physicalAddress"],bookData["title"],bookData["author"],
                    bookData["publicationDate"],state,bookData["occupiedOrReservedBy"],bookData["UUID"])

    # Member Functions 
    def MoveBook(self,newPhysicalAddress):
        self.m_PhysicalAddress = newPhysicalAddress
    
    def ChangeState(self,newState):
        self.m_State = newState

    # Might user be reader
    def ReserveBook(self,user):
        self.ChangeState(BookState.RESERVED)
        self.m_OccupiedOrReservedBy = user
        self.UpdateDatabase()

    def OccupyBook(self,user):
        self.ChangeState(BookState.OCCUPIED)
        self.m_OccupiedOrReservedBy = user
        self.UpdateDatabase()

    def FreeBook(self):
        self.ChangeState(BookState.FREE)
        self.m_OccupiedOrReservedBy = None
        self.UpdateDatabase()
    
    def UpdateDatabase(self):
        # Database Query
        DatabaseHandler().UpdateBook(self)
        pass


