from webServer import *
import sqlite3

def setFound(id):
    mydb = sqlite3.connect("ducksDB.db")
    cursor = mydb.cursor()

    cursor.execute("SELECT id FROM ducks WHERE longid = %s;" % (id))
    shortid = cursor.fetchone()[0] + 1

    cursor.execute("SELECT found FROM ducks WHERE longid = %s;" % (id))
    isFound = cursor.fetchone()[0]
    if isFound == 1:
        message = "Duck %d has already been found." % (shortid)
        return loadFile("indexFound.html",(message,))

    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()

    message = "You have found duck %d!" % (shortid)
    return loadFile("indexFound.html",(message,))

def getDucks():
    mydb = sqlite3.connect("ducksDB.db")
    cursor = mydb.cursor()
    
    cursor.execute("SELECT found FROM ducks")
    result = cursor.fetchall()
    data = ""
    for x in result:
        data += str(x[0])
    return data

if __name__ == "__main__":
    methods = {"f":(setFound,["id"]),
               "getDucks":(getDucks,[])}

    server = WebServer(8350,methods)
    server.start()

#Improve website, send ideas to maddy etc
#style for mobile 
#remove print statements

#images dont work - glitched probably due to wwifi
    #get usb ethernet

#write duck numbers



#Eventually - before deployment:
#remove db from git - put in gitignore