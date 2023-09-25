import os
import socket
from time import *
import threading
from datetime import datetime
import traceback

class WebServer:
    def __init__(self,port,methods):
        self.port = port
        self.methods = methods

    def start(self):
        print('Web Server starting on port: %d...' % (self.port))

        servSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            servSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            servSocket.bind(('0.0.0.0',self.port))
            servSocket.listen(1)
            while True:
                print("waiting")
                connSocket,sourceAddr = servSocket.accept()
                if(connSocket):
                    print("%s connected" %(sourceAddr[0]))
                    newThread = threading.Thread(target=self.handleRequest,args=(connSocket,))
                    newThread.start()

        except Exception as e:
            servSocket.close()
            print(e)
            writeError("Connection","",e)

    def handleRequest(self,client):
        print("Handling request")
        
        message = client.recv(1024)
        request = message.decode()
        while(len(message) == 1024):
            sleep(0.01)
            message = client.recv(1024)
            request += message.decode()
            print(len(message))
    
        if(request):
            request = request.split('\n')[0]
            print("Request received: %s" %(request))
            words = request.split()
            url = words[1][1:]

            path = os.getcwd()
            files = os.listdir(path + "/website")

            print(url)
            if(url == "/" or url == ""):
                url = "index.html"

            if(url in files):
                try:
                    file = open(path + "/website/" + url)
                    fileContent = file.read()
                    file.close()

                    servResponse = 'HTTP/1.0 200 OK\n\n' + fileContent
                except Exception as e:
                    writeError("File not found",request,e)
                    servResponse = 'HTTP1/0 404 NOT FOUND\n\nFile Not Found'
            else:
                methodParams = url.split("?")
                methodName = methodParams[0]
                if(methodName in self.methods.keys()):
                    if(len(methodParams) == 2):
                        params = methodParams[1].replace("~"," ").split("&")
                    else:
                        params = []
                    paramsDict = dict(param.split("=") for param in params)

                    if(set(self.methods[methodName][1]).issuperset((paramsDict.keys()))):
                        try:
                            result = str(self.methods[methodName][0](**paramsDict))
                            servResponse = 'HTTP/1.0 200 OK\n\n' + result
                        except Exception as e:
                            writeError("Method error",request,e)
                            print("ERROR: METHOD ERROR")
                            servResponse = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
                    else:
                        print("ERROR: Params are not suitable for requested method")
                        servResponse = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
                else:
                    print("ERROR: File/Method not found")
                    servResponse = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

            client.sendall(servResponse.encode())
            print("Request handled")
            
        client.close()
    
def writeError(type,request,exception):
    now = datetime.now()

    current_time = now.strftime("%d:%m:%Y   %H:%M:%S")

    f = open("debug.txt","a")
    f.write("TIME:     " + current_time + "\nTYPE:     " + type + "\nREQUEST:     " + request + "\nEXCEPTION:     " + str(exception) + "\nTRACEBACK:     ")
    f.writelines(traceback.format_exc())
    f.write("\n\n\n")
    f.close()
    

#customize error messages
#account for more errors
#prevent server crashing, put in try except

#rename repo and files

#track unique vissits
#track unique users
#track user locations

#feature for bug report/crash report



#after a crash, doesnt respond, should do as in new thread