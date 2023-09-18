from webServer import *
import mysql.connector

#put details in file and read rather than plaintext
mydb = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "SebSmith2002!",
    database = "ducks"
)

cursor = mydb.cursor()

def setFound(id):
    print("here")
    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()
    print("finished")

if __name__ == "__main__":
    methods = {"setFound":(setFound,["id"])}

    server = WebServer(8350,methods)
    server.start()

#ctrl c on web server doesnt update until refresh