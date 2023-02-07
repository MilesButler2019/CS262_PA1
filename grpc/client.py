import os
import chat_pb2
import chat_pb2_grpc
import time
import grpc


def run():
    with grpc.insecure_channel("localhost:9999") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        while True:
            