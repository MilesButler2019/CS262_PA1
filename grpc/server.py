from concurrent import futures
import grpc
import chat_pb2
import chat_pb2_grpc
import time
import threading
from collections import defaultdict
import datetime



class Listener(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.accounts = {"test":"test","test1":"test1"}
        self.all_inbox = {}
        self.user_sessions = []
        self.user_session = None


    def getUsers(self,request,context):
        for i in self.accounts.keys():
            creds = chat_pb2.Credentials()
            creds.username = i
            time.sleep(.1)
            yield creds

      

    def CreateAccount(self, request, context):
        if request.username in self.accounts:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='user name already exists')
            return reply
        else:
            try:
                self.accounts[request.username] = request.password
                self.all_inbox[request.username] = defaultdict(list)
                
                for i in range(10):
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    self.all_inbox[request.username]["Server"] = []
                    default_message = chat_pb2.Message(content="Welcome say something nice",sent_time=formatted_datetime,src = "Server",dest=request.username)
                    self.all_inbox[request.username]["Server"].append(default_message)
                self.user_session = request.username
                self.user_sessions.append(request.username)
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account Created Sucsessfully')
                return reply
            except:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error Creating Account, Try Again')
                return reply

    def LogIn(self, request, context):
        #  try and die login methd 
        try:
            if self.accounts[request.username] ==  request.password:
                self.user_session = request.username
                self.user_sessions.append( request.username)
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Login Success')
                return reply
            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='bad password')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='incorrect username')
            return reply

    def LogOut(self, request, context):
        try:
            reply = chat_pb2.AccountStatus(AccountStatus=1,message="You are sucsessfully logged out")
            self.user_sessions.remove(self.user_session)
            self.user_session = None
            return reply
        except:
            reply = chat_pb2.AccountStatus(AccountStatus=0,message="Error logging out")
            return reply


    def DeleteAccount(self,request,context):
        try:
            if request.username in self.accounts:
                del self.accounts[request.username]
                del self.user_sessions[self.user_sessions.index(request.username)]
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account deleted successfully')
                return reply
            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Account not Found')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error in your request')
            return reply
    
    def getInbox(self, request, context):
        if self.user_session in self.accounts:
            for i,v in self.all_inbox[self.user_session].items():
                for mes in self.all_inbox[self.user_session][i]:
                    time.sleep(.1)
                    yield mes
        else:
            reply = chat_pb2.Message(content="User not found",sent_time="today",dest = request.dest,src="server")
            return reply

                
            

        

# Transform to CHat
    def SendChat(self, request_iter, context):
            for request in request_iter:
                try:
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%d-%Y %H:%M")
                    message = chat_pb2.Message(content=request.content,sent_time=formatted_datetime,src=self.user_session,dest=request.dest)
                    if self.all_inbox[request.dest][request.src]:
    
                        self.all_inbox[request.dest][request.src].append(message)
                    else:
                        # if request.dest not in self.accounts:
                            # message = chat_pb2.MessageStatus(message_status=0,message="Error Sending Messag - User doesn't exist")
                            # yield message
                        self.all_inbox[request.dest][request.src] = []
                        self.all_inbox[request.dest][request.src].append(message)
                    # self.all_inbox[request.src][request.dest].append(message)
                    message = chat_pb2.MessageStatus(message_status=1,message="Message Sent")
                    yield message
                except:
                    message = chat_pb2.MessageStatus(message_status=0,message="Error Sending Message")
                    yield message
   
        

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  chat_pb2_grpc.add_ChatServiceServicer_to_server(
      Listener(), server)
  server.add_insecure_port('localhost:9999')
  server.start()
  server.wait_for_termination()

if __name__ == "__main__":
    serve()