# Write up of design decisions, failed attempts, debugging work, etc.



## Design Decisions
We first started with a simple Client - Server approach to grasp our understanding of sockets although we quickly realized that we wanted to have a server that could handle multiple clients at once. We did some research and found out that we needed to use a Thread for each client. We also started out by using a dictionary to hold account and password information. 



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

We attempted to send the data as a serialized string and many issues trying to read it on the server side as a dict. We ended up using the buil in eval method in python to read the data in as a dict


## Tests

The Edge Cases we cover were

- Creating and Deleting Account
- Creating Duplicate Accounts
- Deleteing Non Existing Account