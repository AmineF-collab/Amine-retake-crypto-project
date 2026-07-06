import socket
class Server:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, Ip_address, port):
        self.client.connect(Ip_address,port)
        print(f'Connected on {Ip_address}:{port}')

    def send_message(self, msg, type_msg):
        packet = (msg, type_msg)
        self.client.sendall(packet)
        print('Message sent')

    def receive(self):
        pass
    
    def close(self):
        self.client.close