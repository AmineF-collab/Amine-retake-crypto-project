from cryptography.hazmat.primitives import hashes
def SHA_256(msg):
    return hashes.SHA256(msg)