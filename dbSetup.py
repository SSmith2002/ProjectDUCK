import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "SebSmith2002!",
    database = "ducks"
)

cursor = mydb.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS ducks (id INTEGER, longid INTEGER, found BOOLEAN)")


