import socket
import configuration
import sys
import os
from threading import Thread
host = configuration.host
port = configuration.port
class Client():
    def __init__(self):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def CLI(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Client started (not connected yet).\n Type /help to see available commands, or /connect to connect to the server.')
        while True :
            command = input("\n> ")
            if command == "/help" :
                print("/help")
                print("/connect")
                print("/disconnect")
                print("/generate_keys <username>")
                print("/send_text <username> <object_name> <message>")
                print("/listaf")
                print("/get <object_id>")
                print("/verify <object_id>")
                print("/verify_all")
                print("/tamper <object_id>")
                print("/exit")
            if command == "/connect" :
                try:
                    self.client.connect((host,port))
                    print("Connected to server 127.0.0.1:6000")
                except OSError:
                    print("You are already connected")
        
            if command == "/disconnect" :
                self.client.close()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Disconnected from server")
            if command == "/generate_keys <username>" :
                pass
            if command == "/send":
                self.send_message()
                print(self.receive)
            if command == "/listaf":
                pass
            if command == "/get <object_id>":
                pass
            if command == "/verify <object_id>":
                pass
            if command == "/verify_all":
                pass
            if command == "/tamper <object_id>":
                pass
            if command == "/exit":
                self.client.close()
                sys.exit()
    def send_message(self):
        message = input("\n>")
        self.client.sendall(message.encode())
        

    def receive(self):
        client_message = self.client.recv(1024).decode()
        if not client_message:
            return None
        return client_message.decode()
    
Client = Client()
Client.CLI()