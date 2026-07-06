
print('Client started (not connected yet).\n Type /help to see available commands, or /connect to connect to the server.')
command = input("\n> ")
if command == "/help" :
    print("/help")
    print("/connect")
    print("/disconnect")
    print("/generate_keys <username>")
    print("/send_text <username> <object_name> <message>")
    print("/list")
    print("/get <object_id>")
    print("/verify <object_id>")
    print("/verify_all")
    print("/tamper <object_id>")
    print("/exit")



