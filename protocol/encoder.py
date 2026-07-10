import json
def encode(payload:dict):
    return json.dumps(payload).encode("utf-8")