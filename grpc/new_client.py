import os
import chat_pb2
import chat_pb2_grpc
import time
import grpc
import datetime
import threading


class Client:

    def __init__(self,):
        # Username and Password
        self.username = None
        self.password = None 
        # create a gRPC channel + stub
        channel = grpc.insecure_channel("localhost:9999")
        self.conn = chat_pb2_grpc.ChatServiceStub(channel)
        #Flag to see if user is logged in
        self.logged_in_status = False
        #Person you want to chat with
        self.chat_thread = None
        self.messages_on_demand = []
        #Event to kill on demand sending
        self.stop_event = threading.Event()
        #Event to Chat stream on demand sending
        self.chat_thread_stop_event = threading.Event()
   
    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        while not self.chat_thread_stop_event.is_set():
            for note in self.conn.ChatStream(chat_pb2.StreamRequest(id=1,src=self.username,dest=self.chat_thread)):  # this line will wait for new messages from the server!
                print("R[{}] {} \n".format(note.src, note.content))  # debugging statement
                # self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # add the message to the UI

    def send_message(self):
        """
        This method is called when user enters something into the textbox
        """
        # message = self.entry_message.get()  # retrieve message from the UI
        
        dest = input("Who would you like to message? ")
        dest_status = self.conn.CheckUserOnline(chat_pb2.Request(username=dest))
        print(dest_status.message)
        if dest_status.message ==  "User doesn't exist":
                return
        if dest_status.message ==  "User Offline":
            self.message_loop(dest,True)
        else:
            self.chat_thread = dest
            # while self.chat_thread_stop_event 
            threading.Thread(target=self.__listen_for_messages, daemon=True).start()
            self.message_loop(dest,False)
            self.chat_thread_stop_event.set()
          # send the Note to the server

            

    def message_loop(self,dest,wait: bool):
        while True:
            message = input("Enter Message (exit to quit) \n")
            if message != '':
                if message == 'exit':
                    break
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                n = chat_pb2.Message()  # create protobug message (called Note)
                n.src = self.username  # set the username
                n.dest = dest
                n.content = message  # set the actual message of the note
                n.sent_time = formatted_datetime
                # print("S[{}] {}".format(n.src, n.content))  # debugging statement
                if wait:
                    #Add messages to be sent later
                    self.messages_on_demand.append(n)
                else:
                    #Send messages
                    self.conn.SendChat(n)
        if wait:
            #On demand messages
            self.background()
        else:
            #Kill the chat thread
            self.chat_thread_stop_event.set()
        
    def deliver_on_demand(self):
        time.sleep(60)

        while not self.stop_event.is_set():
            for i in self.messages_on_demand:
                self.conn.SendChat(i)
            self.stop_event.set()


    def background(self):
        threading.Thread(target=self.deliver_on_demand, daemon=True).start()

    def login(self):
        while self.logged_in_status != True:
            rpc_call = input("Welcome to the chat server! Please type 1 to login or 2 to create an account: ")

            login_indicator = False
            if rpc_call in ["1","2"]:
                while login_indicator != True:
                    username = input("Please Enter your username: ")
                    password = input("Please Enter your password: ")
                    
                    creds = chat_pb2.Credentials(username=username,password=password)

                    if rpc_call == "1":
                        delayed_reply = self.conn.LogIn(creds)
                        print(delayed_reply.message)
                        
                        if delayed_reply.AccountStatus == 1:
                            #Exit when log in sucsess
                            self.logged_in_status = True
                            self.username = username
                            self.password = password
                            break
  
                    if rpc_call == "2":
                        delayed_reply = self.conn.CreateAccount(creds)
                        print(delayed_reply.message)
                        if delayed_reply.AccountStatus == 1:
                            #Exit when log in sucsess
                            self.logged_in_status = True
                            self.username = username
                            self.password = password
                            break

    def exit_logout(self):
        req = chat_pb2.Request(username=self.username)
        reply = self.conn.LogOut(req)
      
    def main_menu(self):
        while True:
                rpc_call = input("Type LS to list all users, MSG to send a message, INBOX to see your messages, LOGOUT to logout, DEL to delete your account, ACC for acount information: ")
                if rpc_call.lower() == "ls":
                    #Add try excepts here for robustness and uptime
                    get_users = chat_pb2.Request(request_status=1)
                    get_users_reply = self.conn.getUsers(get_users)
                    for i in get_users_reply:
                        print(i)
                if rpc_call.lower() == "logout":
                    req = chat_pb2.Request(username=self.username)
                    reply = self.conn.LogOut(req)
                    print(reply.message)
                    if reply.AccountStatus == 1:
                        break

                if rpc_call.lower() == "msg":
                    self.send_message()
                    
            
                if rpc_call.lower() == "inbox":
                        # rpc_call = input("Who do you want to chat with? ")
                    user = chat_pb2.Request(username=self.username)
                    server_reply = self.conn.getInbox(user)
                    for i in server_reply:
                        print("----------------","\n","From:",i.src,"on:",i.sent_time,"\n","\n",i.content,"\n")
                        # print(delayed)
                if rpc_call.lower() == "del":
                    #Add try excepts here for robustness and uptime
                    confirm = input("Are you sure you want to delete your accont? (y/n)")
                    if confirm.lower() == 'y':
                        username = input("Please Enter your username: ")
                        password = input("Please Enter your password: ")
                        creds = chat_pb2.Credentials(username=username,password=password)
                        server_reply = self.conn.DeleteAccount(creds)
                        print(server_reply.message)
                        if server_reply.AccountStatus == 1:
                            break
    
def main():
    try:
        c = Client()
        c.login()
        c.main_menu()
    except:
        #Logs user out on termination
        c.exit_logout()

main()
