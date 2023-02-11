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
        self.all_inbox = defaultdict(list)
        self.user_session = None


    def getUsers(self,request,context):
        for i in self.accounts.keys():
            creds = chat_pb2.Credentials()
            creds.username = i
            time.sleep(.2)
            yield creds


      

    def CreateAccount(self, request, context):
        print(request.username)
        print(request.password)
        if request.username in self.accounts:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='user name already exists')
            return reply
        else:
            try:
                self.accounts[request.username] = request.password
                self.all_inbox[request.username] = []
                for i in range(10):
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    default_message = chat_pb2.Message(content="Welcome say something nice",sent_time=formatted_datetime,src = "Server",dest=request.username)
                    self.all_inbox[request.username].append(default_message)
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account Created Sucsessfully')
                return reply
            except:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error Creating Account, Try Again')
                return reply

    def LogIn(self, request, context):
        #  try and die login methd 
        try:
            if self.accounts[request.username] ==  request.password:
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Login Success')
                return reply
            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='bad password')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='incorrect username')
            return reply


    def DeleteAccount(self,request,context):
        try:
            if request.username in self.accounts:
                del self.accounts[request.username]
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account deleted successfully')
                return reply
            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Account not Found')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error in your request')
            return reply
    
    def getInbox(self, request, context):
        
        if request.username in self.accounts:
            for i in self.all_inbox[request.username]:
                yield i
        else:
            reply = chat_pb2.Message(content="User not found",sent_time="today",dest = request.dest,src="server")
            return reply

                
            

        

# Transform to CHat
    def SendChat(self, request_iter, context):
            for request in request_iter:
                try:
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    message = chat_pb2.Message(content=request.content,sent_time=formatted_datetime,src=request.src,dest=request.dest)
                    # self.all_inbox[request.recipient][]  = 
                    message = chat_pb2.MessageStatus(message_status=1,message="Message Sent")
                    yield message
                except:
                    message = chat_pb2.MessageStatus(message_status=0,message="Error Sending Message")
                    yield message
            # return reply
                # print("blah")
                # print(request.recipient)
                # print(request.content)
                # print(request.sent_time)
                # if request.username in self.accounts:
                    # auth_mesg = chat_pb2.AuthMessage(message = 'user name already exists')

    
        
    #         delayed_reply.AccountStatus = 1
    #         return delayed_reply

            
    #         # return delayed_reply
    #         # if request_iter.username in self.accounts:
    #         #     print('user name already exists')
    #         #     return chat_pb2.AccountStatus(AccountStatus=0)
    #         # else:
    #         #     self.accounts[request_iter.username] == request.password
    #         #     return chat_pb2.AccountStatus(AccountStatus=1)
            
            
        

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  chat_pb2_grpc.add_ChatServiceServicer_to_server(
      Listener(), server)
  server.add_insecure_port('localhost:9999')
  server.start()
  server.wait_for_termination()

if __name__ == "__main__":
    serve()