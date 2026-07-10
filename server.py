import socket
import configuration
import uuid
import time
import os
import base64
import json
from protocol import frame, decoder, encoder
from configuration import type_submit, type_list, type_get, type_tamper, type_ok, type_error
host = configuration.host
port = configuration.port

server_storage = "server_storage"
class Server:
    def __init__(self):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client= None
        os.makedirs(server_storage, exist_ok=True)
        
    def start(self):
        self.server.bind((host,port))  
        self.server.listen()
         
    def connect(self):
        self.client, addresse = self.server.accept()
        print('Received connection request from', addresse)
        self.receive(self.client)

    def send_message(self, message:str):
            self.client.sendall(message.encode())

    def receive(self, client_socket):
        while True:
            try:
                msg_type, raw_payload = frame.recv_msg(client_socket)
            except ConnectionError:
                print("Client disconnected")
                break

            payload = decoder.decode(raw_payload)
            print(f"\033[1;31;40mClient[{msg_type}]: command={payload.get('command')}\033[0m")

            
            print("DEBUG: entering try block")
            response_type, response_payload = self.commande_handler(msg_type, payload)
            data = encoder.encode(response_payload)
            frame.send_msg(client_socket, response_type, data)
            

    def commande_handler(self,message_type, payload):
        if message_type == type_submit:
             return self.submit_handler(payload)
        elif message_type == type_list:
             pass
        elif message_type == type_get:
             pass
        elif message_type == type_tamper:
             pass
        else:
            return type_error, f"Unknown message type {message_type}"
        
    def submit_handler(self, payload):
         if payload.get("command") != "SEND_SIGNED_TEXT":
              return type_error, "type and command mismatch"
         
         object_id = str(uuid.uuid4())
         object_dir = os.path.join(server_storage,object_id)
         os.makedirs(object_dir, exist_ok=True)

         message_bytes = base64.b64decode(payload["message_b64"])
         signature_bytes = base64.b64decode(payload["signature_b64"])
         public_key_pem = base64.b64decode(payload["public_key_b64"]).decode()

         metadata = {
              "object_id": object_id,
              "object_name": payload["object_name"],
              "sender": payload["sender"],
              "has_algorithm": payload["hash_algorithm"],
              "timestamp": time.time(),
              "tampered": False
         }

         with open(os.path.join(object_dir, "content.bin"),"wb") as f:
            f.write(message_bytes)
         with open(os.path.join(object_dir, "signature.bin"),"wb") as f:
            f.write(signature_bytes)
         with open(os.path.join(object_dir, "public_key.pem"),"wb") as f:
            f.write(public_key_pem.encode())

         with open(os.path.join(object_dir, "metadata.json"), "w") as f:
              json.dump(metadata, f, indent=2)

         return type_ok,{"status": "OK", "object_id": object_id}


         
 
    def close(self):
        self.server.close

server1 = Server()
server1.start()
print(f"Server started on {host}:{port}\nWaiting for clients...")
server1.connect()


