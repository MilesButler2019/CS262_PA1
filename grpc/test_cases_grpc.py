import unittest
import chat_pb2
import chat_pb2_grpc
import grpc
import client
from unittest.mock import patch
from io import StringIO 
import sys
import signal
import uuid

# def connect():
#     with grpc.insecure_channel("localhost:9999") as channel:
#         stub = chat_pb2_grpc.ChatServiceStub(channel)
#     return stub

#Client Tests

class TestCreateDuplicate(unittest.TestCase):
    @patch('builtins.input', side_effect=["2","john_lvi","doe"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        try:
            client.run()
        except: 
            self.assertIn('user name already exists\n', str(sys.stdout.getvalue()))

class TestCreateReg(unittest.TestCase):
    @patch('builtins.input', side_effect=["2",str(uuid.uuid4()),"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            client.run()
        except: 
            self.assertIn('Account Created Sucsessfully\n', str(sys.stdout.getvalue()))

class TestDeleteBasic(unittest.TestCase):
    account = str(uuid.uuid4())
    @patch('builtins.input', side_effect=["2",account,"test",de])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            client.run()
        except: 
            self.assertIn('Account Created Sucsessfully\n', str(sys.stdout.getvalue()))


class TestLogin(unittest.TestCase):
    @patch('builtins.input', side_effect=["1","john_lvi","doe"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            client.run()
        except: 
            self.assertIn('Login Success\n', str(sys.stdout.getvalue()))

class TestLogout(unittest.TestCase):
    @patch('builtins.input', side_effect=["1","john_lvi","doe","logout"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            client.run()
        except: 
            self.assertIn('You are sucsessfully logged out\n', str(sys.stdout.getvalue()))




    
if __name__ == '__main__':
    print(unittest.main())