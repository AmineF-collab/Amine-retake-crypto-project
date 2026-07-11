import socket
import configuration
import json
import base64
import sys
from crypto import rsa_keys, signature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from protocol import frame, encoder, decoder
from configuration import type_submit, type_list, type_get, type_tamper
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
                    print(f"Use /generate_keys <username>")
                    continue
                username = balise[1]
                self.generate_keys(username)

            if cmd == "/send":
                if len(balise)<4:
                    print("Use :/send <username> <object_name> <message>")
                    continue
                username = balise[1]
                object_name = balise[2]
                message = balise[3]
                self.send_text(username,object_name,message)
            if cmd == "/list":
                self.list_objects()
            if cmd == "/get":
                if len(balise)<2:
                    print("Use /get <object_id>")
                    continue
                response = self.get_object(balise[1])
                print(response)
                if response.get("status")== "OK":
                    message_bytes = base64.b64decode(response["message_b64"])
                    signature_bytes = base64.b64decode(response["signature_b64"])
                    public_key_pem = base64.b64decode(response["public_key_b64"])
                    public_key = load_pem_public_key(public_key_pem)
                    boolean_response = signature.verify(message_bytes, signature_bytes, public_key)
                    print(f"Signature: {'VALID' if boolean_response else 'INVALID'}")

            if cmd == "/verify":
                if len(balise)<2:
                    print("Utilisez /verify <object_id>")
                    continue
                self.verify_object(balise[1])
            if cmd == "/verify_all":
                self.verify_all()
            if cmd == "/tamper":
                if len(balise)<2:
                    print("Usage: /tamper <object_id>")
                    continue
                self.tamper_object(balise[1])
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

        msg_type, encoded_response = frame.recv_msg(self.client)
        response = decoder.decode(encoded_response)
        print(response)
        

    def generate_keys(self,username:str):
        private_key, public_key = rsa_keys.generate_keys()
        self.keys[username] = {"private_key": private_key, "public_key": public_key}
        print(f"Key generated for {username}")

    def get_object(self, object_id:str):
        payload = {"command": "GET_OBJECT", "object_id": object_id}
        send_payload = encoder.encode(payload)
        frame.send_msg(self.client, type_get, send_payload)
        msg_type, encoded_response = frame.recv_msg(self.client)
        response = decoder.decode(encoded_response)
        return response
    
    def list_objects(self):
        payload = {"command": "LIST_OBJECTS"}
        send_payload = encoder.encode(payload)
        frame.send_msg(self.client, type_list, send_payload)
        msg_type, encoded_response = frame.recv_msg(self.client)
        response = decoder.decode(encoded_response)
    
        objects = response.get("objects", [])
        if not objects:
            print("No objects found.")
        for obj in objects:
            print(f"- {obj['object_id']} | name={obj['object_name']} | sender={obj['sender']} | tampered={obj['tampered']}")
        return objects
    
    def verify_object(self,object_id):
        response = self.get_object(object_id)
        if response.get("status") != "OK":
            print(f"Error: {response}")
            return False
        object_name = response["metadata"]["object_name"]
        message_bytes = base64.b64decode(response["message_b64"])
        signature_bytes = base64.b64decode(response["signature_b64"])
        public_key_pem = base64.b64decode(response["public_key_b64"])
        public_key = load_pem_public_key(public_key_pem)

        boolean_response = signature.verify(message_bytes, signature_bytes, public_key)
        print(f"Object {object_id}")
        print(f"Message: {message_bytes.decode(errors='replace')}")
        print(f"Signature: {'VALID' if boolean_response else 'INVALID'}")
        return boolean_response
    
    def verify_all(self):
        objects = self.list_objects()
        object_number = 0
        sum_valid = 1
        print(f"\nVerifying {len(objects)} objects")
        for obj in objects:
            print(f"Object number:{object_number}\n")
            object_number += 1
            object_id = obj["object_id"]
            validation = self.verify_object(object_id)
            print(f"{object_id}, {obj["object_name"]}, {validation}\n")
            if validation:
                sum_valid+=1
        print(f"\nSummary: {sum_valid}/{len(objects)} valid")

    def tamper_object(self, object_id: str):
        payload = {"command": "TAMPER_OBJECT", "object_id": object_id}
        send_payload = encoder.encode(payload)
        frame.send_msg(self.client, type_tamper, send_payload)
        msg_type, encoded_response = frame.recv_msg(self.client)
        response = decoder.decode(encoded_response)
        print(response)
            
        
        

    def receive(self):
        client_message = self.client.recv(1024).decode()
        if not client_message:
            return None
        return client_message.decode()
    
Client = Client()
Client.CLI()