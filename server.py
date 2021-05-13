import json
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Client():
    def __init__(self,uName,client,BUFSIZ):
        self.username = uName
        self.client = client
        self.BUFSIZ = BUFSIZ
        self.connected = True
        self.THREAD = Thread(target=self.recieveMsg())
        self.THREAD.start()

    def recieveMsg(self):
        while self.connected:
            self.Rmessage = self.client.recv(self.BUFSIZ).decode("utf8")
            self.readMessage(self.Rmessage)


    def sendMsg(self,Smessage):
        self.client.send(bytes(Smessage, "utf8"))
    
    def readMessage(self,RRmessage):
        self.RRmessage = RRmessage
        self.deserialised = json.loads(self.RRmessage)
        if self.deserialised["identifier"] == "directMessage":
            self.directMessage(self.deserialised["message"],self.deserialised["recipient"])
        self.sendMsg(self.RRmessage)
    def directMessage(self,DMmessage,DMrecipient):
        self.DMmessage = DMmessage
        self.DMrecipient = DMrecipient
        try:
            clients[self.DMrecipient].sendall(bytes(self.DMmessage, "utf8"))
            #wait for same message to be sent back
        except:
            return False


        

def login(data):
    if data["requestID"] != "loginRequest":
        print("ALERT! Login request invalid")
        return False
    username = data["username"]
    #password = data["password"]
    #check with database, and if correct then return true
    return username



def comsInit():
    while True:
        client, client_address = SERVER.accept() 
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



# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""

#     for sock in clients:
#         sock.send(bytes(prefix, "utf8")+msg)

        
clients = {} # {username:clientObj}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=comsInit)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()