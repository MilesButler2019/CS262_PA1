import socket
import argparse
# Add command line arguments
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server



if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-t", "--type", help="Request type")
    args = parser.parse_args()
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    if args.type:
        request_type = args.type
    message = "{'request_type':" + request_type + ", 'username':'" + username + "', 'password':'" + password + "'}"

     # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)

    print(f"Received {data!r}")