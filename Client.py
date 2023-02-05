import socket
import argparse
# Add command line arguments
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server



if __name__ == "__main__":

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.settimeout(10)
        while True:
            # receive data from the server
            data = s.recv(1024).decode('utf-8')
            # take user input
            user_input = input(data)
            server_version = "0"
            request_type = "0"
            message = "{'server_version':" + server_version + ",'request_type':" + request_type + ", 'data':'" + user_input + "'}"
            s.sendall(message.encode('utf-8'))
 

    # print(f"Received {data!r}")