import socket
import configuration
import json
import base64
import sys
from crypto import rsa_keys, signature
from cryptography.hazmat.primitives import serialization
from protocol import frame, encoder, decoder
from configuration import type_submit
host = configuration.host
port = configuration.port

class Client():
    def __init__(self):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keys = {}
        
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
            if cmd == "/generate_keys":
                if len(balise)<2:
                    print(f"Username = {balise[1]}")
                    continue
                username = balise[1]
                self.generate_keys(username)

            if cmd == "/send":
                if len(balise)<4:
                    print("Utilisez cette command :/send <username> <object_name> <message>")
                    continue
                username = balise[1]
                object_name = balise[2]
                message = balise[3]
                self.send_text(username,object_name,message)
            if cmd == "/list":
                pass
            if cmd == "/get <object_id>":
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
    
    def send_text(self, username, object_name:str, message:str):
        if username not in self.keys:
            print(f"no keys found for {username} do /generate_keys first")
            return
        private_key = self.keys[username]["private_key"]
        public_key = self.keys[username]["public_key"]

        public_key_pem = public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        
        message_bytes = message.encode()
        sign = signature.signature(message_bytes, private_key)
        
        payload = {
            "command": "SEND_SIGNED_TEXT",
            "object_name": object_name,
            "sender": username,
            "message_b64": base64.b64encode(message_bytes).decode(),
            "signature_b64": base64.b64encode(sign).decode(),
            "public_key_b64": base64.b64encode(public_key_pem.encode()).decode(),
            "hash_algorithm": "SHA-256"
        }
        send_payload = encoder.encode(payload)
        frame.send_msg(self.client, type_submit,send_payload)

        msg_type, raw_response = frame.recv_msg(self.client)
        response = decoder.decode(raw_response)
        print(response)
        

    def generate_keys(self,username:str):
        private_key, public_key = rsa_keys.generate_keys()
        self.keys[username] = {"private_key": private_key, "public_key": public_key}
        print(f"Key generated for {username}")

    def receive(self):
        client_message = self.client.recv(1024).decode()
        if not client_message:
            return None
        return client_message.decode()
    
Client = Client()
Client.CLI()