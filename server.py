import socket
import configuration
from threading import Thread
host = configuration.host
port = configuration.port  
class Server:
    def __init__(self):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client= None
        
    def start(self):
        self.server.bind((host,port))  
        self.server.listen()
         
    def connect(self):
            self.client, addresse = self.server.accept()
            print('Received connection request from', addresse)
            self.client.send("has connected".encode())
            self.receive(self.client)

    def send_message(self, message:str):
            self.client.sendall(message.encode())

    def receive(self, client_socket):
        while True:
            client_message = client_socket.recv(1024).decode()
            if not client_message:
                break
            print("\033[1;31;40m" + "Client:" + client_message + "\033[0m")
            response = self.commande_handler(client_message)
            self.send_message(response)

    def commande_handler(self,msg):
        return f"Message reçu {msg}"
 
    def close(self):
        self.server.close

server1 = Server()
server1.start()
print(f"Server started on {host}:{port}\nWaiting for clients...")
server1.connect()


