
import socket
import threading

class ChatServer(object):
    def __init__(self, host):
        #Define the host and port
        self.host = host
        self.port = 65432
        #Create the socket and bind it to the host and port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        #Create a dictionary to store the accounts
        self.accounts = {}

    def listen(self):
        #Listen for connections and start a new thread for each connection

        print("Starting server on port " + str(self.port) + "and listening for connections...")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()


    def listenToClient(self, client, address):
        size = 1024
        print("New connection from " + str(address))
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Decode the data and turn it into a dictionary so we can access it using eval
                    data = eval(data.decode('utf-8'))
                    # Process the request type and get the response
                    response = self.process_request_type(data)
                    # Send the response back to the client and encode it to utf-8
                    client.send(response.encode('utf-8'))
                else:
                    # If there is no data, the client has disconnected
                    raise ConnectionError('Client disconnected')
            except:
                print("Client {} disconnected".format(str(address)))
                client.close()
                return False

    def process_request_type(self,data):
        if data['request_type'] == 0:
            #Create account
            return self.create_account(data)
        
        elif data['request_type'] == 1:
            #Delete account
            return self.delete_account(data)

            #Need to account for the case when there are unread messages

        elif data['request_type'] == 2:
            #Login
            return self.login(data)
        
        elif data['request_type'] == 3:
            #Logout
            return self.logout(data)

        elif data['request_type'] == 4:
            #Send message
            return self.send_message(data)


    def delete_account(self,data):
        if data['username'] in self.accounts:
            del self.accounts[data['username']]
            return "Account deleted successfully"
        else:
            return "Account doesn't exist"

    def create_account(self,data):
        if data['username'] in self.accounts:
            return "Account already exists"
        else:
            self.accounts[data['username']] = data['password']
            return "Account created successfully"

if __name__ == "__main__":
    ChatServer('').listen()