from webServer import *
import sqlite3

def setFound(id):
    mydb = sqlite3.connect("ducksDB.db")
    cursor = mydb.cursor()

    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()

    cursor.execute("SELECT id FROM ducks WHERE longid = %s;" % (id))
    shortid = cursor.fetchone()[0]
    return loadFile("indexFound.html",(shortid+1,))

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

#When finding duck "Duck # already found!" ####

#Improve website, send ideas to maddy etc
#style for mobile ####
#remove print statements

#images dont work - glitched #####



#Eventually - before deployment:
#remove db from git - put in gitignore