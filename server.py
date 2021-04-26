from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def comsInit():
    while True:
        client, client_address = SERVER.accept() 
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please enter your username:", "utf8"))
        username = client.recv(BUFSIZ).decode("utf8")
        #here add database lookup
        client.send(bytes("Please enter your password:", "utf8"))
        password = client.recv(BUFSIZ).decode("utf8")
        #here add a database lookup

        #if username and password both match, connect the user and set their status as online
        Thread(target=User, args=(client,)).start()


class User():
    def __init__(self,client):
        self.client = client
        self.command = self.client.recv(BUFSIZ).decode("utf8")
        #waits for commands from client
        if self.command.startswith("startchat") == True: #command to start a private chat
            pcInit(self.command)

    def pcInit(self,command) #start a private chat with another user specified in the command
        user2name = self.command.lstrip("startchat") #removes the command startchat to isolate the username

        #check if user is in database and is online





def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
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