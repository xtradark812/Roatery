import json
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

class Client():
    def __init__(self,uName,client,BUFSIZ):
        self.username = uName
        self.client = client
        self.BUFSIZ = BUFSIZ
        self.connected = True


    def recieveMsg(self):
        while self.connected:
            self.Rmessage = self.client.recv(self.BUFSIZ).decode("utf8")
            self.read = False
            self.read = self.readMessage(self.Rmessage)
            if self.read == False:
                print("error, message failed to read/send")
                self.sendMsg("error")#send an error object
                
    

    def sendMsg(self,Smessage):
        self.client.send(bytes(Smessage, "utf8"))

    def readMessage(self,Recvmessage):
        self.RRmessage = Recvmessage
        self.deserialisedRR = json.loads(self.RRmessage)
        if self.deserialisedRR["identifier"] == "directMessage":
            DM = self.directMessage(self.RRmessage,self.deserialisedRR["recipient"])
            if DM == False:
                return False
            return True
        else:
            return False
    
    def run(self):
        self.THREAD = Thread(target=self.recieveMsg())
        self.THREAD.start()

    
    def directMessage(self,DMmessage,DMrecipient):
        self.DMmessage = DMmessage
        self.DMrecipient = DMrecipient
        try:
            clients[self.DMrecipient].sendMsg(self.DMmessage)
            return True
        except KeyError: #THIS MEANS USER IS NOT IN USERS DICT
            return False


        
def login(client,client_address):
    #Then wait for login
    loginData = client.recv(BUFSIZ).decode("utf8")
    data = json.loads(loginData)

    if data["requestType"] != "loginRequest":
        print("%s:%s invalid login request." % client_address)
        return False

    else:
        username = data["username"]
        password = data["password"]
        if username in clients.keys():
            loginReq = json.dumps({"requestType":"loginRequest","loginR":False,"reason":"Already logged in"})
            client.send(bytes(loginReq, "utf8")) #add excpetion whch logs out old user
            return False
        else:
            #database lookup here!
            #if username and pass dont mach
                #loginReq = json.dumps({"requestType":"loginRequest","loginR":False,"reason":"Invalid username/password"})
                #client.send(bytes(loginReq, "utf8"))
                #return False
            #elseif username and pass mach
                #print("confirmed login:",loginR,"at","%s:%s" % client_address)
                #loginReq = json.dumps({"requestType":"loginRequest","loginR":True})
                #client.send(bytes(loginReq, "utf8"))
                #return username
            pass
    



def comsInit(client,client_address):
    while True:

        print("%s:%s has connected." % client_address)

        #first wait for handshake
        handshake = client.recv(BUFSIZ).decode("utf8")
        if handshake == "alpha 1.0":
            client.send(bytes(handshake, "utf8"))
            print("%s:%s connection confirmed." % client_address)
        

        loggedIn = False
        while loggedIn == False:
            loggedIn = login(client,client_address)    

        #create client object
        clientObj = Client(loggedIn,client,BUFSIZ)
        #then add client object to the dictionary
        clients.update({loggedIn:clientObj})
        clientObj.run()
        

def initThread():
    while True:
        client, client_address = SERVER.accept() 
        clientThread = Thread(target=comsInit, args=[client,client_address])
        clientThread.start()

    




# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""

#     for sock in clients:
#         sock.send(bytes(prefix, "utf8")+msg)

        
clients = {} # {username:clientObj}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    acceptThread = Thread(target=initThread)
    acceptThread.start()
    acceptThread.join()
    SERVER.close