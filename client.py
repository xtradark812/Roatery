from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import json
import inspect

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj

class Main():
    def __init__(self,cs,bf):
        self.client_socket = cs
        self.BUFSIZ = bf


    def sendMessage(self,message):
        self.message = message
        #add encryption for message here
        self.client_socket.send(bytes(self.message, "utf8"))



class UserLogin(): #userlogin object to send to server
    def __init__(self):
        self.requestID = "loginRequest"
        self.username = self.getUsername()
        self.password = self.getPassword()

    def getUsername(self):
        self.usr = input("Username:") #asks for username
        return self.usr
    
    def getPassword(self):
        self.psw = input("Password:") #asks for password
        return self.psw
        #possibly add hashing for password?

def login(client_socket,BUFSIZ): #when called, attempts to login, and if sucsessful, returns true and sets logged in = true.
    serialized = json.dumps(UserLogin(), cls=ObjectEncoder, indent=2, sort_keys=True) #serialize data
    client_socket.sendall(bytes(serialized, "utf8")) ### SENDS LOGIN DATA TO SERVER [loginRequest,username,password]
    response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
    if response == serialized:
        loggedIn = True
        return True
    else:
        print("ERROR! Invalid response from server")
        return False

def handshake(client_socket,BUFSIZ):
    data = "alpha 1.0"
    client_socket.send(bytes(data, "utf8")) ### SENDS DATA TO SERVER "handshake"
    response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
    if response == data:
        return True

#INIT CONNECTION (function?)
def initcon():
    HOST = "127.0.0.1" #input('Enter host: ')
    PORT = "33000" #input('Enter port: ')

    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    #HANDSHAKE
    while handshake(client_socket,BUFSIZ) != True:
        print("Attempting to verify connection...")
        time.sleep(5)
    #LOGIN
    loggedIn = False
    while loggedIn == False:
        loggedIn = login(client_socket,BUFSIZ)

    if loggedIn == True:
        Main(client_socket,BUFSIZ)


initcon()

        

