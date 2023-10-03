from webServer import *
from dbDetails import mydb

cursor = mydb.cursor()

def setFound(id):
    cursor.execute("UPDATE ducks SET found = TRUE WHERE longid = %s;" % (id))
    mydb.commit()
    return loadFile()

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

#Research and buy raspberry pi zero 2w
    #Power
    #How to connect external IO
    #Connect to monitor

#When finding duck, popup to say "Duck # found!" or "Duck # already found!"
#When call setFound, load index
#Have ducks say their number

#Improve website, send ideas to maddy etc




#RPI products


#https://thepihut.com/products/raspberry-pi-zero-2?variant=41181426909379

#Wireless mouse and keyboard? https://thepihut.com/products/super-compact-wireless-keyboard-and-mouse
#Case and heatsink
#SD Card - Should already have
#USB hub? #https://thepihut.com/collections/raspberry-pi-usb-accessories/products/usb-mini-hub-with-power-switch-otg-micro-usb
#HDMI cable https://thepihut.com/products/mini-hdmi-to-hdmi-cable-v1-4-zero?variant=31762478465086
#Power supply https://thepihut.com/products/raspberry-pi-zero-uk-power-supply
#USB shim if only need wireless adapter - https://thepihut.com/products/usb-to-microusb-otg-converter-shim

