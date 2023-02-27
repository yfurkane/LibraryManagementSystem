from enum import Enum
import uuid
from User import *


class MainHandler:
    #Constructor
    def __init__(self):
        self.m_DatabaseHandler = DatabaseHandler() #Singeleton Class
        self.m_DatabaseHandler.Init(db_file = "libraryDb (2).sqlite")

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
                self.SignUp() # TO DO
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
            if (idCounter > 3):#3 kezden farklı yanlış girilirse dışarı atıyor.
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
        
    


def main():

    mainHandler = MainHandler()
    mainHandler.Start()


if __name__ == "__main__":
    main()