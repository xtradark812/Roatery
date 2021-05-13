from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import json
import inspect
import re

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
        self.quitapp = False
        self.THREAD = Thread(target=self.recieveMsg())
        self.commandLine()

    def recieveMsg(self):
        while not self.quitapp:
            self.Rmessage = self.client_socket.recv(self.BUFSIZ).decode("utf8") 
            #needs to read the message and print it
            
    
    def commandLine(self):
        while not self.quitapp:
            self.usersOnline()
            self.command = input(">")

            if self.command.startswith("send") == True:
                self.recipientMessage = self.command.replace('send', '')
                self.recipient = self.recipientMessage.split()[0]
                self.message = self.recipientMessage.replace(self.recipient,'',1).lstrip()
                self.serialized = json.dumps(newMessage(self.recipient,self.message), cls=ObjectEncoder, indent=2, sort_keys=True)
                self.client_socket.sendall(bytes(self.serialized, "utf8")) ### SENDS MESSAGE TO SERVER
                self.response = self.client_socket.recv(self.BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
                if self.response == self.serialized:
                    print("Message sent sucsessfully")


            elif self.command == "help":
                print("Commands:")
                print("send [username] [message] - send a secure message to [username]")
                print("quit - ends the session")

            elif self.command == "quit":
                self.quitapp = True


    def usersOnline(self):
        pass # will request a list of online friends from the server and print it.

            
class newMessage():
    def __init__(self,recipient,message):
        self.identifier = "directMessage"
        self.recipient = recipient
        self.message = message
    
    




class LoginRequest(): #LoginRequest object to send to server
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
    serialized = json.dumps(LoginRequest(), cls=ObjectEncoder, indent=2, sort_keys=True) #serialize data
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

        

