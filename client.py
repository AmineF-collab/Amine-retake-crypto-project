import socket
import server
import exemple
def client():
    host = exemple.host
    port = exemple.port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                server.server1.connect
                client.connect((host,port))
                print("Connected to server 127.0.0.1:6000")
            except OSError:
                print("You are already connected")
        
        if command == "/disconnect" :
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Disconnected from server")
        if command == "/generate_keys <username>" :
            pass
        if command == "/send_text <username> <object_name> <message>":
            pass
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
            pass

client()