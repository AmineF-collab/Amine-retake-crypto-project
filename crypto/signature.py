from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import rsa_keys
private_key = rsa_keys.private_key
def signature(message:str,private_key: RSAPrivateKey):
    signature = private_key.sign(message,padding.PKCS1v15,hashes.SHA256)
    return signature

