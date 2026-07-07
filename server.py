import socket
host = '127.0.0.1'
port = 6000
print("Server started on 127.0.0.1:6000\nWaiting for clients...")

connected = True   


class Server:
    def __init__(self):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        self.server.bind((self.host,port))  
        self.server.listen()
         
    def connect(self):
        while True:
            client_arrive, addresse = self.server.accept
            print(f"Connected with {addresse}")
            client_arrive.send(f"T'es connecté au server".encode('ascii'))
            self.server.sendto("oui".encode('ascii'),addresse)
    def send_message(self, msg, type_msg):
        packet = (msg, type_msg)
        self.server.sendall(packet)
        print('Message sent')

    def receive(self):
        while True:
            self.server.recv
    
    def close(self):
        self.client.close

server1 = Server()
server1.start()
print("Serveur a start normalement")