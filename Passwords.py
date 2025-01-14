from argon2 import PasswordHasher 
from argon2.exceptions import VerifyMismatchError 
ph = PasswordHasher() 
#This is needed to encrypt and check for proper credentials

def login(user, storedHash, enteredPassword):
    #if user in database:
        try:
            ph.verify(storedHash, enteredPassword)
            print("Login successful!")
        except VerifyMismatchError:
            print("Incorrect password.")
        except Exception as error:
            print(f"An error occurred: {error}")
    #else: 
        #print("Invalid user or W#.")   #I'll refine this as I figure out how to actually use the 'users' info


#Simply put, mismatch just sees if the hashes dont match, verify checks if they do, the exception is for anything else

def registerUser(): 
    user = input("Enter username/W#: ")
    return user

def registerPass():
    enteredPassword = input("Enter password: ")
    hashed = ph.hash(enteredPassword) 
    return hashed 
#Needs a way to push these values to database as a pair

user = registerUser()
testPass = registerPass()
passAttempt = input("Enter your password: ")
login(user, testPass, passAttempt)
#generic layout of operations, again to be refined as more of it comes together