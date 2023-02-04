import socket
import argparse
# Add command line arguments
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server



if __name__ == "__main__":

    # args = parser.parse_args()
    # if args.username:
    #     username = args.username
    # if args.password:
    #     password = args.password
    # if args.type:
    #     request_type = args.type
    # 



     # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024).decode('utf-8')
            user_input = input(data)
            server_version = "0"
            request_type = "0"
            message = "{'server_version':" + server_version + ",'request_type':" + request_type + ", 'data':'" + user_input + "'}"
            s.sendall(message.encode('utf-8'))
        # s.sendall(message.encode('utf-8'))
        # data = s.recv(1024)

    # print(f"Received {data!r}")