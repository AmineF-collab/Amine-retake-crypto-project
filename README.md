Amine-retake-crypto-project

Objectives : 
- Implement a TCP Server that stores signed objects on disk, lists them, serves them back on request, and can intentionally tamper with stored content
- Implement Client that generate keys and then create signed object and send them to the server and that can receive and verify them back
- Security goal: integrity (detect if a message changed after signing) and origin linking (tie a message to the key that signed it)

Project Structure:
signed_exchange_project/
 
 |-- server.py
 |-- client.py 
 |-- configuration.py 
 |
 |-- protocol/ 
 | |-- frame.py
 | |-- encoder.py
 | |-- decoder.py 
 | 
 |-- crypto/ 
 | |-- hashing.py 
 | |-- rsa_keys.py 
 | |-- signature.py 
 | 
 |-- server_storage/ 
 (If an object was already sent) 
 | |-- object_1/ 
 | | |--message.bin 
 | | |--metadata.json 
 | | |--public_key.pem 
 | | |--signature.bin
 
Requirements: pip install cryptography

How to run the program:
- First start the server:

  use Python server.py in the terminal

  expected :

  Server started on 127.0.0.1:6000

  Waiting for clients...

- Then start the client :

  use Python client.py

  expected :

  Client started (not connected yet).

  Type /help to see available commands, or /connect to connect to the server.

- Connect the client to the server:

  use /connect

  expected :

  Received connection request from ('127.0.0.1', 65061) ---> in the server side

- Generate the private and public keys:

  use /generate_keys "<username>"

  expected :

  Key generated for "<username>"

- Send signed text:

  use /send_text "<username>" "<object_name>" "<message>"

  expected :

  Client side : {'status': 'OK', 'object_id': 'object_1'}

  Server side : Client[83]: command=SEND_SIGNED_TEXT

The object will appear in the folders server_storage:

<img width="301" height="115" alt="image" src="https://github.com/user-attachments/assets/31e39ca1-dfbc-4832-8762-4698d0757a9b" />

In the core_payload you can find the information of the object you sent

<img width="322" height="181" alt="image" src="https://github.com/user-attachments/assets/4d00ec7e-0cc9-443c-bbd2-0c2ed122f6ec" />

In the message.bin, the message you sent

<img width="267" height="45" alt="image" src="https://github.com/user-attachments/assets/05665e0a-baae-4767-82aa-19084cbc11d2" />

In public_key.pem, the public key in pem format

<img width="561" height="211" alt="image" src="https://github.com/user-attachments/assets/7f579f38-e4f0-46fc-ad94-3b0ea6c0ef56" />

In the signature.bin, the signature of the message with the private key you can't see it as if it were text, because it's raw binary bytes.

- Then you can get the object you just send:

  with /get <object_id> --> use the object_id you received after you sent the object

  expected :

  <img width="953" height="211" alt="image" src="https://github.com/user-attachments/assets/638ef330-b030-4896-b1cb-b6d856c44cdb" />


 

  
  


