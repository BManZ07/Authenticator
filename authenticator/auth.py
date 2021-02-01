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

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Authenticator",
    auth_plugin="mysql_native_password"
)

myCursor = db.cursor()
DB_NAME = "Authenticator"



input("Please enter your username: ")

def authCode(n):
    letterLower = list(string.ascii_lowercase)
    letterUpper = list(string.ascii_uppercase)
    number = list(string.digits)
    punctuation = ['!', "#", "$", "@", "%", "^", "&", "*"]
    combined = letterLower + letterUpper + number + punctuation
    combinedJoin = ''.join(combined)

    resString = ''.join(random.choices(combinedJoin, k=n))
    return resString



