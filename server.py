import json
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading



class Client():
    def __init__(self,uName,client,BUFSIZ):
        self.username = uName
        self.client = client
        self.BUFSIZ = BUFSIZ
        self.connected = True
        self.THREAD = Thread(target=self.recieveMsg())
        self.THREAD.start()
        print("test1")

    def recieveMsg(self):
        while self.connected:
            self.Rmessage = self.client.recv(self.BUFSIZ).decode("utf8")
            self.read = False
            self.read = self.readMessage(self.Rmessage)
            if self.read == True:
                self.sendMsg(self.Rmessage)
            elif self.read == False:
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
        

    
    def directMessage(self,DMmessage,DMrecipient):
        self.DMmessage = DMmessage
        self.DMrecipient = DMrecipient
        try:
            if self.DMrecipient == self.username:
                print("Message sent sucsessfully to",self.username)
            else:
                clients[self.DMrecipient].sendMsg(self.DMmessage)
            return True
        except KeyError: #THIS MEANS USER IS NOT IN USERS DICT
            return False


        
def login(data):
    if data["requestID"] != "loginRequest":
        print("ALERT! Login request invalid")
        return False
    username = data["username"]
    #password = data["password"]
    #check with database, and if correct then return true
    return username



def comsInit(client,client_address):
    while True:
        print("%s:%s has connected." % client_address)

        #first wait for handshake
        handshake = client.recv(BUFSIZ).decode("utf8")
        if handshake == "alpha 1.0":
            client.send(bytes(handshake, "utf8"))
            print("%s:%s connection confirmed." % client_address)
        
        #Then wait for login
        loginData = client.recv(BUFSIZ).decode("utf8")
        deserialized = json.loads(loginData)
        loggedIn = False
        while loggedIn == False:
            loggedIn = login(deserialized)
        if loggedIn != False:
            print("confirmed login:",loggedIn,"at","%s:%s" % client_address)
            client.send(bytes(loginData, "utf8"))

        #if username and password both match, create a client object
        clientObj = Client(loggedIn,client,BUFSIZ)
        #then add client object to the dictionary
        clients.update({loggedIn:clientObj})
        
        #set status as online?


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