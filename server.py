from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def login(data):
    if data[0] != "loginRequest":
        print("ALERT! Login request invalid")
        return False
    username = data[1]
    password = data[2]
    #check with database, and if correct then return true
    return True



def comsInit():
    while True:
        client, client_address = SERVER.accept() 
        print("%s:%s has connected." % client_address)
        #first wait for handshake
        handshake = client.recv(BUFSIZ).decode("utf8")
        if handshake == "alpha 1.0":
            client.send(bytes(handshake, "utf8"))
            print(client, "handshake confirmed")
        
        loginData = client.recv(BUFSIZ).decode("utf8")

        loggedIn = False
        while loggedIn == False:
            loggedIn = login(loginData)

        #if username and password both match, connect the user
        clients.update({loginData[1]:client})
        
        #set status as online?



# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""

#     for sock in clients:
#         sock.send(bytes(prefix, "utf8")+msg)

        
clients = {} # {username:client}
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