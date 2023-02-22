import socket
import threading
from collections import defaultdict
import datetime


class ChatServer(object):
    def __init__(self, host):
        #Define the host and port
        self.host = host
        self.port = 65432
        self.server_version = 0
        # self.encoding_type = 'utf-8'
        #Create the socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set the socket to reuse the address
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Bind the socket to the host and port
        self.sock.bind((self.host, self.port))
        #Create a dictionary to store the accounts
        self.accounts = {}
        #Variable to track the current user
        self.user_session = None
        #Create a dictionary to store the inbox
        self.all_inbox = defaultdict(list)
        


    def process_request(self, client):

        #Wire protocol
        #Decode the data and turn it into a dictionary so we can access it using eval
        while True:
            response = client.recv(1024).decode('utf-8')
            response = eval(response)
            
            if response['server_version'] != self.server_version:
                client.send("Invalid server version".encode('utf-8'))
                client.close()
                return False
            # if response['encoding_type'] != self.encoding_type:
            #     client.send("Invalid encoding type".encode('utf-8'))
            #     client.close()

            return response['payload']

    def listen(self):
        #Listen for connections and start a new thread for each connection
        print("Starting server on port " + str(self.port) + "and listening for connections...")

        #Listen for connections and start a new thread for each connection totalled to 5 connections
        self.sock.listen(5)

        while True:
            client, address = self.sock.accept()
            #Set the socket timeout to 5 minutes
            client.settimeout(300)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()



    def listenToClient(self, client, address):
        print("New connection from " + str(address))
        #Send the welcome message
        while True:
            self.welcome(client)
        # self.welcome(client)
   

    def welcome(self,client):
         #Send Welcome Message and ask for login or create account
        welcome = "Welcome to the chat server! Please type 1 to login or 2 to create an account: "
        client.send(welcome.encode('utf-8'))
                    
        response = self.process_request(client)
        if response == "1":
                #Login and with username and password
            self.login(client,response)
    
        elif response == "2":
                #create account with username and password
            self.create_account(client,response)
            

                
    
    #Chat Menu is only accessible after login or create account
    def chat_menu(self,client):
        while True:
            print(self.user_session, "is logged in")
            client.send("Type LS to list all users, MSG to send a message, INBOX to see your messages, LOGOUT to logout, DEL to delete your account: ".encode('utf-8'))
            response = self.process_request(client)
            if response.lower() == "ls":
                self.list_users(response,client)
            elif response.lower() == "msg":
                self.send_message(response,client)
            elif response.lower() == "inbox":
                self.inbox(response,client)
            elif response.lower() == "logout":
                self.logout(response,client)
            elif response.lower() == "del":
                self.delete_account(self.user_session,client)
            elif response.lower() == "session":
                client.send(str(self.user_session).encode('utf-8'))
            else:
                client.send("Invalid input".encode('utf-8'))

    def login_menu(self,client,data):
        # Login Menu to get username and password
        client.send("Please enter your username: ".encode('utf-8'))
        username = self.process_request(client)
        client.send("Please enter your password: ".encode('utf-8'))
        password = self.process_request(client)
        data = {'username':username, 'password':password}
        return data

    def create_account(self,client,data):
        creds = self.login_menu(client,data)
        #Check if account already exists
        if creds['username'] in self.accounts:
            client.send("Account already exists \n".encode('utf-8'))
        #Create account if it doesn't exist
        else:
            self.accounts[creds['username']] = creds['password']
            #Set the user session to the username
            self.user_session = creds['username']
            self.all_inbox[creds['username']] = []
            client.send("Account created successfully hit enter to confirm\n".encode('utf-8'))
            self.process_request(client)
            self.chat_menu(client)
                    


    def login(self,client,data):
        #Login Menu to get username and password
        creds = self.login_menu(client,data)
        print(creds)
        #Check if account exists
        if creds['username'] in self.accounts:
            #Check if password is correct
            if self.accounts[creds['username']] == creds['password']:
                client.send("Login successful hit enter to confirm\n".encode('utf-8'))
                self.process_request(client)
                #Set the user session to the username
                self.user_session = creds['username']
                self.chat_menu(client)
                
            #If password is incorrect
            else:
                client.send("Incorrect password \n".encode('utf-8'))
                self.welcome(client)
        #If account doesn't exist
        else:
            client.send("Account doesn't exist \n".encode('utf-8'))
            self.welcome(client)
          
        
    def logout(self,data,client):
        client.send("Logging out... hit enter to confirm\n".encode('utf-8'))
        self.user_session = None
        self.process_request(client)
        self.welcome(client)

    def list_users(self,data,client):
        output = ""
        for i in self.accounts.keys():
            output += i + "\n"
        output += "hit enter to confirm\n"
        client.send(output.encode('utf-8'))
        self.process_request(client)

    def delete_account(self,data,client):
        if data in self.accounts:
            del self.accounts[data]
            client.send("Account deleted successfully hit enter to confirm\n".encode('utf-8'))
            self.process_request(client)
            self.welcome(client)
        else:
            client.send("Account doesn't exist \n".encode('utf-8'))

    def send_message(self,data,client):
        client.send("Please enter the username of the person you want to send a message to: ".encode('utf-8'))
        username = self.process_request(client)
        client.send("Please enter the message you want to send: ".encode('utf-8'))
        message = self.process_request(client)
        self.all_inbox[username].append({'from':username,'content':message,'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        client.send("Message sent successfully hit enter to confirm\n".encode('utf-8'))
        self.process_request(client)
        self.chat_menu(client)
    
    def inbox(self,data,client):
        print(self.all_inbox[self.user_session])
        output = ""
        for i in self.all_inbox[self.user_session]:
            output += "------------------------------------------\n"
            output += "From: " + i['from'] + "\n"
            output += "Content: " + i['content'] + "\n"
            output += "Time: " + i['time'] + "\n"
            output += "------------------------------------------\n"

        output += "Press enter to confirm\n"
        client.send(output.encode('utf-8'))
        self.process_request(client)

 



if __name__ == "__main__":
    ChatServer('').listen()