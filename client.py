from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


class Main():
    def __init__(self):
        self.handshakeVar = False 
        while self.handshakeVar != True:
            print("Waiting for connection to be cofirmed...")
            self.handshakeVar = self.handshake()
            time.sleep(10)
        if self.handshakeVar == True:
            print("Connection sucsessful.")

        self.login = UserLogin()
        if self.login.loggedIn == True:
            print("login sucsessful")
    
    def handshake(self):
        self.data = "alpha 1.0"
        client_socket.send(bytes(self.data, "utf8")) ### SENDS DATA TO SERVER "handshake"
        self.response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
        if self.response == self.data:
            return True
        

    def sendMessage(self,message):
        self.message = message
        #add encryption for message here
        client_socket.send(bytes(self.message, "utf8"))
        if self.message == "{quit}":
            pass # add quit function
        pass



class UserLogin():
    def __init__(self):
        loggedIn = False
        while loggedIn != True:
            self.username = self.getUsername()
            self.password = self.getPassword()
            self.login()
        
        #add verification?

    def getUsername(self):
        self.usr = input("Username:") #asks for username
        return self.usr
    
    def getPassword(self):
        self.psw = input("Password:") #asks for password
        return self.psw
        #possibly add hashing for password?

    def login(self): #when called, attempts to login, and if sucsessful, returns true and sets logged in = true.
        self.data = []
        self.data.append("loginRequest")
        self.data.append(self.username)
        self.data.append(self.password)
        client_socket.send(bytes(self.data, "utf8")) ### SENDS LOGIN DATA TO SERVER [loginRequest,username,password]
        self.response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
        if self.response == self.data:
            self.loggedIn = True
            return True
        else:
            return False


#INIT CONNECTION (function?)

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

connection = Main()

# receive_thread = Thread(target=Main)
# receive_thread.start()

    


        

