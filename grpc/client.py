import os
import chat_pb2
import chat_pb2_grpc
import time
import grpc
import datetime




def client_login_stream_requests(user):
    while True:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        text = input("Please Enter your message: ")
        if text == "":
            break
        # time.sleep(1)
        message = chat_pb2.Message(content=text,sent_time= formatted_datetime,dest=user.username)
        yield message
        # time.sleep(1)



def run():
    with grpc.insecure_channel("localhost:9999") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        #Login
        while True:
            rpc_call = input("Welcome to the chat server! Please type 1 to login or 2 to create an account: ")

            login_indicator = False
            if rpc_call in ["1","2"]:
                while login_indicator != True:
                    username = input("Please Enter your username: ")
                    password = input("Please Enter your password: ")
                    
                    creds = chat_pb2.Credentials(username=username,password=password)

                    if rpc_call == "1":
                        delayed_reply = stub.LogIn(creds)
                        print(delayed_reply.message)
                        
                        if delayed_reply.AccountStatus == 1:
                            #Exit when log in sucsess
                            login_indicator = True
                        else:
                            break
                    if rpc_call == "2":
                        delayed_reply = stub.CreateAccount(creds)
                        print(delayed_reply.message)
                        if delayed_reply.AccountStatus == 1:
                            #Exit when log in sucsess
                            login_indicator = True
                        else:
                            break
            else:
                print("Invalid Input")
            
            if login_indicator:       
                while True:
                    rpc_call = input("Type LS to list all users, MSG to send a message, INBOX to see your messages, LOGOUT to logout, DEL to delete your account, ACC for acount information: ")
                        

                    if rpc_call.lower() == "ls":
                        #Add try excepts here for robustness and uptime
                        get_users = chat_pb2.Request(request_status=1)
                        get_users_reply = stub.getUsers(get_users)
                        for i in get_users_reply:
                            print(i)
                    if rpc_call.lower() == "logout":
                        print("You are sucsessfully logged out")
                        break

                    if rpc_call.lower() == "msg":
                        rpc_call = input("Who do you want to chat with? ")
                        user = chat_pb2.Request(username=rpc_call)
                        server_reply = stub.getInbox(user)
                        for i in server_reply:
                            print(i.sent_time,i.content)
                        delayed = stub.SendChat(client_login_stream_requests(user))
                        for i in delayed:
                            print(i.message)

                    if rpc_call.lower() == "inbox":
                        # rpc_call = input("Who do you want to chat with? ")
                        user = chat_pb2.Request()
                        server_reply = stub.getInbox(user)
                        for i in server_reply:
                            print(i.sent_time,i.content)
                        # print(delayed)
                    if rpc_call.lower() == "del":
                        #Add try excepts here for robustness and uptime
                        confirm = input("Are you sure you want to delete your accont? (y/n)")
                        if confirm.lower() == 'y':
                            username = input("Please Enter your username: ")
                            password = input("Please Enter your password: ")
                            creds = chat_pb2.Credentials(username=username,password=password)
                            server_reply = stub.DeleteAccount(creds)
                            print(server_reply)
                            if server_reply.AccountStatus == 1:
                                break
                            


                    # else:
                        # print("Invalid Input")
                    # print(delayed_reply.creds.message)
                    #Add try excepts or while loops here for robustness and uptime
                    
            

if __name__ == "__main__":
    run()