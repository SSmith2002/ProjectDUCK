import os
import socket
from time import *
import threading
from datetime import datetime
import traceback
import sys

class WebServer:
    def __init__(self,port,methods):
        self.port = port
        self.methods = methods

    def start(self):
        print('Web Server starting on port: %d...' % (self.port))

        servSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        servSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        servSocket.bind(('0.0.0.0',self.port))
        servSocket.listen(1)
        servSocket.settimeout(0.5)

        try:
            while True:
                try:
                    connSocket,sourceAddr = servSocket.accept()
                    if(connSocket):
                        print("%s connected" %(sourceAddr[0]))
                        newThread = threading.Thread(target=self.handleRequest,args=(connSocket,))
                        newThread.start()
                except KeyboardInterrupt:
                    pass
                except socket.timeout:
                    pass
                except Exception as e:
                    servSocket.close()
                    print(e)
                    writeError("Connection","",e)
                    break

        except:
            print("Keyboard Interrupt")
            servSocket.close()
            sys.exit(0)

    def handleRequest(self,client):
        print("Handling request")
        client.settimeout(0.5) #may cause errors later
        try:
            message = client.recv(1024)
        except socket.timeout:
            print("Request Timed out")
            return
        request = message.decode()
        while(len(message) == 1024):
            sleep(0.01)
            message = client.recv(1024)
            request += message.decode()
            print(len(message))
        
        if(request):
            headersR = request.split('\n')
            request = headersR[0]
            headersDict = createHeadersDict(headersR[1:])
            accept = headersDict["Accept"]
            contentType = accept.split('/')
            print("Request received: %s" %(request))
            words = request.split()
            url = words[1][1:]

            headers = {"Access-Control-Allow-Origin":"*"}
            headerString = ""
            for key in headers.keys():
                headerString += "%s:%s\n" % (key,headers[key])
            headerString += '\n'

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

                    servResponse = 'HTTP/1.0 200 OK\n' + headerString + fileContent
                except Exception as e:
                    writeError("File not found",request,e)
                    servResponse = 'HTTP1/0 404 NOT FOUND\n' + headerString +  'File Not Found'
                client.sendall(servResponse.encode())
            elif contentType[0] == "image":
                splitRequest = url.split('/')
                imageName = splitRequest[-1]
                print(imageName)
                image = open(path + "/website/images/" + imageName,'rb')
                imageContent = image.read()
                print("Image Length: " + str(len(imageContent)))
                image.close()
                headers["Content-Type"] = "image/png"

                client.send(('HTTP/1.0 200 OK\n' + headerString).encode())
                client.sendall(imageContent)
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
                            servResponse = 'HTTP/1.0 200 OK\n' + headerString + result
                        except Exception as e:
                            writeError("Method error",request,e)
                            print("ERROR: METHOD ERROR")
                            servResponse = 'HTTP1/0 404 NOT FOUND\n' + headerString +  'File Not Found'
                    else:
                        print("ERROR: Params are not suitable for requested method")
                        servResponse = 'HTTP1/0 404 NOT FOUND\n' + headerString +  'File Not Found'
                else:
                    print("ERROR: File/Method not found")
                    servResponse = 'HTTP1/0 404 NOT FOUND\n' + headerString +  'File Not Found'

                client.sendall(servResponse.encode())
            print("Request handled")
        
        client.close()
        return

def loadFile(fileName="index.html",vars=()):
    path = os.getcwd()
    files = os.listdir(path + "/website")

    fileContent = None
    if(fileName in files):
        file = open(path + "/website/" + fileName)
        fileContent = file.read()
        file.close()

    if len(vars) > 0:
        fileContent = replaceFiller(fileContent,vars)

    return fileContent

def replaceFiller(content,vars):
    if len(vars) > 0:
        counter = 0
        for i in range(len(content)):
            if content[i:i+3] == "###":
                content = content[:i] + str(vars[counter]) + content[i+3:]
                counter +=1 
                if counter == len(vars):
                    break
        return content
    else:
        return content


def createHeadersDict(headersList):
    headersDict = {}
    for header in headersList:
        index = header.find(":")
        headersDict[header[:index]] = header[index+2:]
    return headersDict



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

#after a crash, doesnt respond, should do as in new thread
#cant download images from inspect element