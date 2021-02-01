"""
To-Do:
- Take Username Input
- Create random 16 character code
- Return code 
- Add code and username to file
- Integrate a database
"""

import string
import random
import mysql.connector
import pyAesCrypt
import config as cfg

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Authenticator",
    auth_plugin="mysql_native_password"
)

myCursor = db.cursor()
#myCursor.execute("CREATE DATABASE Authenticator")
DB_NAME = "Authenticator"

TABLES = {}
TABLES['tokens'] = (
    "CREATE TABLE `tokens` ("
    "  `personID` int(11) NOT NULL,"
    "  `username` varchar(14) NOT NULL,"
    "  `token` varchar(32) NOT NULL"
    ") ENGINE=InnoDB")

#table_description = TABLES['tokens']
#myCursor.execute(table_description)
#b.commit()

def accountCheck():
    hasAccount = input("Do you have an existing account? Yes/No - ")
    if hasAccount == "Yes" or hasAccount == "yes" or hasAccount == "y":
        userName = input("Please enter your username: ")
        hasID = input("Please enter your ID: ")
        if cfg.useAdminAccount == False:
            query = myCursor.execute("SELECT * FROM tokens WHERE username= %s AND personID= %s",(userName, hasID))
            for x in myCursor:
                encryptFile(x[2])
                return "Your token is: " + x[2]

        else:
            if userName == cfg.adminUsername and hasID == cfg.adminPassword:
                myCursor.execute("SELECT * FROM tokens")
                selection = []
                for x in myCursor:
                    selection.append(x)
                print(selection) 

                doDelete = input("Do you wish to revoke a token? Yes/No ")
                if doDelete == "Yes" or doDelete == "yes" or doDelete == "y":
                    whoDelete = input("Username to delete: ")
                    codeDlete = input("ID to delete: ")

                    myCursor.execute("DELETE FROM tokens WHERE username= %s AND personID= %s",(whoDelete, codeDlete))
                    db.commit()
                    return f"User {whoDelete} has been removed!"

    elif hasAccount == "No" or hasAccount == "no" or hasAccount == "n":
        createAccount = input("Do you wish to create an account? Yes/No - ")
        if createAccount == "Yes" or createAccount == "yes" or createAccount == "y":
            userName = input("Please enter your username: ")
            id = random.randint(100000, 999999)
            tokenCode = authCode(32)
            myCursor.execute("INSERT INTO tokens (personID, username, token) VALUES (%s, %s,%s)", (id, userName, tokenCode))
            db.commit()
            return f"""
            User created:
            Username: {userName}
            ID: {id}
            Token: {tokenCode}
            """
        else:
            exit()
            

def authCode(n):
    letterLower = list(string.ascii_lowercase)
    letterUpper = list(string.ascii_uppercase)
    number = list(string.digits)
    punctuation = ['!', "#", "$", "@", "%", "^", "&", "*"]
    combined = letterLower + letterUpper + number + punctuation
    combinedJoin = ''.join(combined)

    resString = ''.join(random.choices(combinedJoin, k=n))
    return resString

def encryptFile():
    fileName = input("Input file name: ")
    bufferSize = 64 * 1024 
    password = cfg.encryptionToken
    pyAesCrypt.encryptFile(f"authenticator\{fileName}", f"authenticator\{fileName}.aes", password, bufferSize)
    return f"{fileName} was encrypted"


def decryptFile():
    decreptFile = input("Do you want to unlock a file? Yes/No ")
    if decreptFile == "Yes" or decreptFile == "yes" or decreptFile == "y":
        fileName = input("Input file name: ")
        authId = input("Please enter your ID: ")
        authToken = input("Please enter your token: ")

        myCursor.execute("SELECT token FROM tokens WHERE token= %s AND personID= %s",(authToken, authId))

        for i in myCursor:
            data=i
            if data=="error":
                return "Invlaid Token!"
            else:
                bufferSize = 64 * 1024 
                password = cfg.encryptionToken
                pyAesCrypt.decryptFile(f"authenticator\{fileName}.aes", f"authenticator\{fileName}", password, bufferSize)
                return f"{fileName} has been unlocked!"

        

#myCursor.execute("ALTER TABLE tokens MODIFY token VARCHAR(32)")

#print(accountCheck())
print(decryptFile())
#print(encryptFile())


