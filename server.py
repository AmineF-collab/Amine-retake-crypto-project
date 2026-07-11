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
                msg_type, encoded_payload = frame.recv_msg(client_socket)
            except ConnectionError:
                print("Client disconnected")
                break

            payload = decoder.decode(encoded_payload)
            print(f"\033[1;31;40mClient[{msg_type}]: command={payload.get('command')}\033[0m")

            response_type, response_payload = self.commande_handler(msg_type, payload)
            data = encoder.encode(response_payload)
            frame.send_msg(client_socket, response_type, data)
            

    def commande_handler(self,message_type, payload):
        if message_type == type_submit:
             return self.submit_handler(payload)
        elif message_type == type_list:
             return self.list_handler(payload)
        elif message_type == type_get:
             return self.get_handler(payload)
        elif message_type == type_tamper:
             return self.tamper_handler(payload)
        else:
            return type_error, f"Unknown message type {message_type}"
        
    def submit_handler(self, payload):
         if payload.get("command") != "SEND_SIGNED_TEXT":
              return type_error, "type and command mismatch"
         
         object_id = str(uuid.uuid4())
         object_storage = os.path.join(server_storage,object_id)
         os.makedirs(object_storage, exist_ok=True)

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

         with open(os.path.join(object_storage, "content.bin"),"wb") as f:
            f.write(message_bytes)
         with open(os.path.join(object_storage, "signature.bin"),"wb") as f:
            f.write(signature_bytes)
         with open(os.path.join(object_storage, "public_key.pem"),"wb") as f:
            f.write(public_key_pem.encode())

         with open(os.path.join(object_storage, "metadata.json"), "w") as f:
              json.dump(metadata, f, indent=2)

         return type_ok,{"status": "OK", "object_id": object_id}
    
    def get_handler(self,payload):
        if payload.get("command") != "GET_OBJECT":
            return type_error, {"status": "ERROR", "message": "command mismatch"}
        object_id = payload.get("object_id")
        object_storage = os.path.join(server_storage, object_id)
        
        if not os.path.isdir(object_storage):
            return type_error, {"status": "Error", "message": "object not found"}
        with open(os.path.join(object_storage,"content.bin"), "rb") as f:
            message_bytes = f.read()
        with open(os.path.join(object_storage,"signature.bin"), "rb") as f:
           signature_bytes = f.read()
        with open(os.path.join(object_storage,"public_key.pem"), "rb") as f:
            public_key_pem = f.read()
        with open(os.path.join(object_storage,"metadata.json"), "r") as f:
            metadata = json.load(f)
        
        return type_ok,{
            "status": "OK",
            "object_id": object_id,
            "message_b64": base64.b64encode(message_bytes).decode(),
            "signature_b64": base64.b64encode(signature_bytes).decode(),
            "public_key_b64": base64.b64encode(public_key_pem).decode(),
            "metadata": metadata
            }
    
    def list_handler(self, payload):
        if payload.get("command") != "LIST_OBJECTS":
            return type_error, {"status": "ERROR", "message": "command mismatch"}
        objects = []
        if os.path.isdir(server_storage):
            for object_id in os.listdir(server_storage):
                meta_path = os.path.join(server_storage, object_id, "metadata.json")
                if os.path.isfile(meta_path):
                    with open(meta_path, "r") as f:
                        metadata= json.load(f)
                    objects.append(metadata)
        return type_ok, {"status": "OK", "objects": objects}
    
    def tamper_handler(self, payload):
     if payload.get("command") != "TAMPER_OBJECT":
        return type_error, {"status": "ERROR", "message": "command mismatch"}

     object_id = payload.get("object_id")
     object_storage = os.path.join(server_storage, object_id)
     if not os.path.isdir(object_storage):
        return type_error, {"status": "ERROR", "message": "Object not found."}

     content_path = os.path.join(object_storage, "content.bin")
     with open(content_path, "rb") as f:
        data = bytearray(f.read())
     if len(data) > 0:
        data[0] ^= 0xFF 
     with open(content_path, "wb") as f:
        f.write(data)

     meta_path = os.path.join(object_storage, "metadata.json")
     with open(meta_path, "r") as f:
        metadata = json.load(f)
     metadata["tampered"] = True
     with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

     return type_ok, {"status": "OK", "object_id": object_id, "tampered": True}

    def close(self):
        self.server.close

server1 = Server()
server1.start()
print(f"Server started on {host}:{port}\nWaiting for clients...")
server1.connect()


