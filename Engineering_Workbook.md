# Write up of design decisions, failed attempts, debugging work, etc.



## Design Decisions
We first started with a simple Client - Server approach to grasp our understanding of sockets although we quickly realized that we wanted to have a server that could handle multiple clients at once. We did some research and found out that we needed to use a Thread for each client. We also started out by using a dictionary to hold account and password information. Default dict to set a base value of no message in inbox and allow us to have a list for each inbox. 


<img width="655" alt="Screen Shot 2023-02-06 at 2 34 35 PM" src="https://user-images.githubusercontent.com/47306315/217067587-b048d4cf-a0ac-41e3-a63a-d6f97a17228d.png">





## Wire Protocal

We wanted to be as simplistic as possible within our protocal our protical tentativley looks like:

- a version number of our server (int - 4 bytes / 32 bits)
- request ID (operation code) (int - 4 bytes / 32 bits)
- data 

    #### Client side
    This is sent as a dict in string format (in python) and encoded in utf-8 from the client side
    #### Server side
    The server then decoded this information back to a string and then uses the eval method in python to read the request in a dict format



## Failed Attempts

We attempted to send the data as a serialized string and many issues trying to read it on the server side as a dict. We ended up using the buil in eval method in python to read the data in as a dict. 


After Implementing basic functions such as create account and delete account we realized that we shouldn't instantly close the connection in cases where the user user sould login and stay logged in. We have to change how we handle these certain requests. After Implementing User input we also forgot about our original wire protocal and had to go back and modify our code to include it. We ended up almost only implementing the wire protocal 1 way from client to server and not in reverse. We had some issues with the inbox feature as apparently there is a default python method caled inbox after renaming it to all_inbox fixed the issue, and ended up using deafult dict as the datatype. 

On the GRCP side:
We struggled to understand the streaming aspect for a while and eventually figured out how to do streaming in threads. After noticing our laptops were heating up we realized that we must also close the threads. 

Forgot command to recompli .proto file
 Added here for reference
#Command to recomplie if needed
python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/chat.proto 
## Tests

[Our Wire Protocal,GRCP]
The Edge Cases we cover were
- Creating and Deleting Account [,X]
- Creating Duplicate Accounts [,X]
- Deleteing Non Existing Account [,X]
- Logging into Deleted Account [,X]
- When Inbox is empty [,X]
- Inbox when message is sent [,X]
- OnDemand Message with wait time [,X]
- Listing All users [,X]
- Checking that deleted users don't appear in ls [,X]
- Invalid Input from user [,X]
- Messaging someone who doesn't have an account [,X]
- Message with no content [,X]