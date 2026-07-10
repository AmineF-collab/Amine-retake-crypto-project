import socket
import configuration
import json
import base64
import sys
import rsa_keys
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
            balise = command.split(" ",3)
            cmd = balise[0]
            if cmd == "/help" :
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
            if cmd == "/connect" :
                try:
                    self.client.connect((host,port))
                    print("Connected to server 127.0.0.1:6000")
                except OSError:
                    print("You are already connected")
        
            if cmd == "/disconnect" :
                self.client.close()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Disconnected from server")
            if cmd == "/generate_keys <username>" :
                if len(balise)<2:
                    print(f"Username = {balise[1]}")
                    continue
                username = balise[1]
                self.generate_keys(username)

            if cmd == "/send":
                self.send_message()
                print(self.receive)
            if cmd == "/listaf":
                pass
            if cmd == "/get":
                pass
            if cmd == "/verify <object_id>":
                pass
            if cmd == "/verify_all":
                pass
            if cmd == "/tamper <object_id>":
                pass
            if cmd == "/exit":
                self.client.close()
                sys.exit()
    def send_message(self):
        message = input("\n>")
        self.client.sendall(message.encode())

    def generate_keys(self,username:str):
        private_key, public_key = rsa_keys.generate_keys()
        self.keys[username] = {f"private key : {private_key}, public_key : {public_key}"}
        print(f"Key generated for {username}")

    def receive(self):
        client_message = self.client.recv(1024).decode()
        if not client_message:
            return None
        return client_message.decode()
    
Client = Client()
Client.CLI()