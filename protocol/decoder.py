import json

def decode(data: bytes):
    return json.loads(data.decode("utf-8"))