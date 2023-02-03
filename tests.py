import unittest
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432 


def connect_to_server(message):
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)
    return data


#Test cases for creating an account
class TestCreateBasicCreateAndDelete(unittest.TestCase):
    def runTest(self):
        
        #Test creating account
        message = "{'request_type':0, 'username':'username ', 'password':'password'}"
        data = connect_to_server(message)
        self.assertEqual(data,b"Account created successfully","Error creating account")

        #Test deleting account
        message = "{'request_type':1, 'username':'username ', 'password':'password'}"
        data = connect_to_server(message)
        self.assertEqual(data,b"Account deleted successfully","Error deleting account")
      
        

class TestCreateDuplicateAccount(unittest.TestCase):
    def runTest(self):

        #Send same request twice to create duplicate account
        message = "{'request_type':0, 'username':'username ', 'password':'password'}"
        data = connect_to_server(message)
        data = connect_to_server(message)
        self.assertEqual(data,b"Account already exists","Error creating duplicate account")
    
        #Delete Account so that we can continue testing
        message = "{'request_type':1, 'username':'username ', 'password':'password'}"
        data = connect_to_server(message)


#Test cases for deleting an account

class TestDeleteNonExistingAccount(unittest.TestCase):
    def runTest(self):
        message = "{'request_type':1, 'username':'username ', 'password':'password'}"
        data = connect_to_server(message)
        self.assertEqual(data,b"Account doesn't exist","Deleted non existing account")


if __name__ == '__main__':
    unittest.main()