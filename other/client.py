from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import json
import inspect
import re
from datetime import datetime



def login(client_socket,BUFSIZ): #when called, attempts to login, and if sucsessful, returns true and sets logged in = true.
    while True:
        try:
            username = str(input("Enter username: "))
            password = str(input("Enter password: "))
            break
        except:
            print("Invalid Input!")

    loginReq = {"requestType":"loginRequest","username":username,"password":password}
    serialized = json.dumps(loginReq) #serialize data
    client_socket.sendall(bytes(serialized, "utf8")) ### SENDS LOGIN DATA TO SERVER [loginRequest,username,password]
    try:
        response = json.loads(client_socket.recv(BUFSIZ).decode("utf8")) ### WAITS FOR SAME DATA TO BE RETURNED
    except:
        print("Invalid response from server")
    if response["requestType"]=="loginRequest" and response["loggedIn"]==True:
        return username
    else:
        
        return False

def handshake(client_socket,BUFSIZ):
    data = "alpha 1.0"
    client_socket.send(bytes(data, "utf8")) ### SENDS DATA TO SERVER "handshake"
    response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
    if response == data:
        return True

#INIT CONNECTION

if __name__ == "__main__":
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
    if loggedIn != False:
        THREAD2 = Thread(target=commandLine)
        THREAD1 = Thread(target=recieveMsg)
        THREAD1.start()
        THREAD2.start()
        

