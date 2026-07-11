Amine-retake-crypto-project

Objectives : 
- Implement a TCP Server that stores signed objects on disk, lists them, serves them back on request, and can intentionally tamper with stored content
- Implement Client that generate keys and then create signed object and send them to the server and that can receive and verify them back
- Security goal: integrity (detect if a message changed after signing) and origin linking (tie a message to the key that signed it)

Communication Protocol:

We have to send frame with this format:

- `HEADER`:  ASCII `SFX`
- `TYPE`: 1 byte, one of `S` (submit), `L` (list), `G` (get), `T` (tamper), `O` (success), `E` (error)
- `LENGTH`: 4-byte big-endian unsigned int, size of PAYLOAD
- `PAYLOAD`: UTF-8 JSON, max 1 MB
  
Project Structure:
```
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
``` 
Requirements: pip install cryptography

How to run the program:
- First start the server:

  use Python server.py in the terminal

  expected :

  <img width="264" height="33" alt="image" src="https://github.com/user-attachments/assets/2609ea00-d166-4fc7-867c-70c5e71f75cb" />

- Then start the client :

  use Python client.py

  expected :

  <img width="540" height="37" alt="image" src="https://github.com/user-attachments/assets/ea76c491-ff76-4ec4-afdf-de48f4933a61" />

- Connect the client to the server:

  use /connect

  expected :

  <img width="375" height="17" alt="image" src="https://github.com/user-attachments/assets/cb2831d1-7d14-45e4-bd81-d67d91659a08" />

- Generate the private and public keys:

  use ```/generate_keys <username>```

  expected :

  <img width="207" height="36" alt="image" src="https://github.com/user-attachments/assets/5140da7d-02fc-4ec5-9343-5eea1d6e3d1f" />


- Send signed text:

  use ```/send_text <username> <object_name> <message>```

  expected :

  Client side :

  <img width="348" height="33" alt="image" src="https://github.com/user-attachments/assets/1ecc6aaa-d96f-4d3b-9660-5b13fd05e497" />

  Server side :

  <img width="272" height="23" alt="image" src="https://github.com/user-attachments/assets/c7172fb7-7131-44aa-a247-4e88502cd059" />

  The object will appear in the folders server_storage:

  <img width="301" height="115" alt="image" src="https://github.com/user-attachments/assets/31e39ca1-dfbc-4832-8762-4698d0757a9b" />

  In the core_payload you can find the information of the object you just sent:

  <img width="322" height="181" alt="image" src="https://github.com/user-attachments/assets/4d00ec7e-0cc9-443c-bbd2-0c2ed122f6ec" />

  In the message.bin, the message you just sent:

  <img width="267" height="45" alt="image" src="https://github.com/user-attachments/assets/05665e0a-baae-4767-82aa-19084cbc11d2" />

  In public_key.pem, the public key in pem format:

  <img width="561" height="211" alt="image" src="https://github.com/user-attachments/assets/7f579f38-e4f0-46fc-ad94-3b0ea6c0ef56" />

  In the signature.bin, the signature of the message with the private key you can't see it as if it were text, because it's in raw binary bytes.

- Then you can get the object you just send:

  with /get <object_id> --> use the object_id you received after you sent the object

  expected :

  In the client side:

  <img width="953" height="211" alt="image" src="https://github.com/user-attachments/assets/638ef330-b030-4896-b1cb-b6d856c44cdb" />

  In the server side :

  <img width="231" height="21" alt="image" src="https://github.com/user-attachments/assets/bcfe8e1f-b75b-4353-8bf1-528dccfe7304" />

  You can see at the end that it is also verified

- You can also verify it directly:

  use /verify <object_id>

  expected :

  <img width="150" height="72" alt="image" src="https://github.com/user-attachments/assets/af34da6c-9073-4317-8efc-b3423704b8d3" />

   In the server side :

  <img width="231" height="21" alt="image" src="https://github.com/user-attachments/assets/c10d18dc-91b4-46fd-8230-2463053b896d" />

- To check if we corrupt the message we can use the tamper command :

  use /tamper <object_id>

  expected:

  Client side:

  <img width="425" height="37" alt="image" src="https://github.com/user-attachments/assets/1ec153e1-a7da-4db3-bd95-547e7f2d6eee" />

  Server side:

  <img width="240" height="20" alt="image" src="https://github.com/user-attachments/assets/e331136f-ce32-4472-b279-c6b96a837b15" />

- Now send two other object with the same method than above

- And we can see all the object we list command

  use /list

  expected:

  Client side:

  <img width="488" height="80" alt="image" src="https://github.com/user-attachments/assets/9a8e11fd-1641-4fc0-a9bd-79ce53c2744c" />

  Server side:

  <img width="230" height="19" alt="image" src="https://github.com/user-attachments/assets/20f17c04-3f8c-47a6-a8aa-fefd0b7b090d" />

- Too finish we can verify all the objects:

  use /verify_all

  expected:

  Client side:

  <img width="508" height="399" alt="image" src="https://github.com/user-attachments/assets/157a6a5a-fbe7-4a74-9e32-facf13b9aa44" />

  Server side:

  <img width="240" height="73" alt="image" src="https://github.com/user-attachments/assets/13a0c478-4028-422c-bef3-46914957eb86" />

- If you finished you can now exit the program or disconnect the client with ```/exit or /disconnect```

  
  






 

  
  


