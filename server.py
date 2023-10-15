from webServer import *
import sqlite3

def setFound(id):
    mydb = sqlite3.connect("ducksDB.db")
    cursor = mydb.cursor()

    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()
    return loadFile()

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
    methods = {"setFound":(setFound,["id"]),
               "getDucks":(getDucks,[])}

    server = WebServer(8350,methods)
    server.start()

#When finding duck, popup to say "Duck # found!" or "Duck # already found!"
#When call setFound, load index
#Have ducks say their number

#Improve website, send ideas to maddy etc
#style for mobile
#remove print statements

#images dont work - glitched
#dont use accept[4] for accepted images - make headers a dictionary, look for "accepted"



#Eventually - before deployment:
#remove db from git - put in gitignore