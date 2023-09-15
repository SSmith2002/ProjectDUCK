import mysql.connector
import random

mydb = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "SebSmith2002!",
    database = "ducks"
)

cursor = mydb.cursor()
cursor.execute("DROP TABLE IF EXISTS ducks")
cursor.execute("CREATE TABLE ducks (id INTEGER PRIMARY KEY, longid INTEGER, found BOOLEAN)")

for i in range(64):
    firstdigit = random.randint(1,9)
    longid = str(firstdigit)
    for k in range(7):
        digit = random.randint(0,9)
        longid += str(digit)
    
    longid = int(longid)
    print(longid)

    cursor.execute("INSERT INTO ducks VALUES (%d,%d,FALSE)" % (i,longid))

mydb.commit()
