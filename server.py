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
    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()

def getDucks():
    cursor.execute("SELECT found FROM ducks")
    result = cursor.fetchall()
    print(result)
    data = ""
    for x in result:
        data += str(x[0])
    return data

if __name__ == "__main__":
    methods = {"setFound":(setFound,["id"]),
               "getDucks":(getDucks,[])}

    server = WebServer(8350,methods)
    server.start()

#put details in file and read rather than plaintext
#ctrl c on web server doesnt update until refresh
#make website
#fix webServer
#add more headers to webServer
