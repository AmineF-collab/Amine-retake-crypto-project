"Si on veut corrompre manuellement"

path = "server_storage/object_1/message.bin"
with open(path, "rb") as f:
    data = bytearray(f.read())
data[0] ^= 0xFF  
with open(path, "wb") as f:
    f.write(data)