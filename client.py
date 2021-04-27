from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter



class UserLogin():
    def __init__(self):
        while loggedIn != True:
            self.username = self.getUsername()
            self.password = self.getPassword()
        
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
        self.data_serialized = json.dumps(self.data) #serialize data 
        client_socket.send(bytes(self.data_serialized, "utf8")) ### SENDS LOGIN DATA TO SERVER [loginRequest,username,password]
        self.response = client_socket.recv(BUFSIZ).decode("utf8") ### WAITS FOR SAME DATA TO BE RETURNED
        if self.response == self.data:
            loggedIn = True
            return True
        else:
            return False



class Main():
    def __init__(self):
        self.HOST = input('Enter host: ')
        self.PORT = input('Enter port: ')
        if not self.PORT:
            self.PORT = 33000
        else:
            self.PORT = int(PORT)

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.login = UserLogin()
        if self.login.login() == True: #attempts to log in to server
            self.receive_thread = Thread(target=self.receive)
            self.receive_thread.start()

    def receive():
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
            except OSError:  # Possibly client has left the chat.
                break

    


        






#------------------------------- THE STUFF BELOW THI LINE IS JUST FOR REFRENCE, NOT FOR THE ACTUAL CODE




def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

#-------------