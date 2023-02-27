from enum import Enum
from user import *


class MainHandler:
    #Constructor
    def __init__(self):
        self.m_DatabaseHandler = DatabaseHandler() #Singeleton Class
        self.m_DatabaseHandler.init(db_file = "libraryDb (2).sqlite")

    #Connect Database
    # Member Function
    def start(self):
        print("Welcome to Library Application")
        print("To exit from application any time enter ':q'")
        while True:
            selection = input("To Log in enter 1, To Sign up enter 2 : ")
            if selection == "1":
                self.auth()
                self.m_LoggedInUser.dialog()              
                break
            elif selection == "2":
                self.signUp() # TO DO
                break
            elif selection == ":q":
                print("Quit")
                break
            else:
                print("Invalid entry")
                continue

    def auth(self):
        #Check Database
        #Get User role
        #Create user
        pwCounter = 0
        idCounter = 0
        while True:
            if (idCounter > 3):#3 kezden farklı yanlış girilirse dışarı atıyor.
                print("Too many wrong username try!")
                MainHandler.shutdown()
            username = input("Username: ")
            if not (self.m_DatabaseHandler.check_user_name(username)):
                print("Invalid username! Does not find any record")
                idCounter +=1
                continue

            while True:
                if (pwCounter > 3):
                    print("Too many wrong password try!")
                    MainHandler.shutdown()

                password = input("Password: ")
                userData = self.m_DatabaseHandler.check_auth(username,password)
                if (userData == None):
                    print("Invalid password try again")
                    pwCounter+=1
                    continue
                else:
                    break
                
            self.m_LoggedInUser = UserFactory.createUser(userData)
            break
    
        
    
    def shutdown():
        print("Exiting..")
        exit()
        
    


def main():

    mainHandler = MainHandler()
    mainHandler.start()


if __name__ == "__main__":
    main()