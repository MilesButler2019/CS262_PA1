from concurrent import futures
import grpc
import chat_pb2
import chat_pb2_grpc
import time
import threading
from collections import defaultdict


class Listener(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.accounts = {"test":"test","test1":"test1"}
        self.all_inbox = defaultdict(list)
        self.user_session = None


    def getUsers(self, request, context):
        for i in self.accounts.keys():
            creds = chat_pb2.Credentials()
            creds.username = i
            yield creds


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  chat_pb2_grpc.add_ChatServiceServicer_to_server(
      Listener(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

if __name__ == "__main__":
    serve()