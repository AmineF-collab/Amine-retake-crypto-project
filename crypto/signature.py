from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
def signature(message:bytes,private_key: RSAPrivateKey):
    signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
    return signature

def verify(message:bytes , signature : bytes, public_key:RSAPublicKey):
    try: 
        public_key.verify(signature,message,padding.PKCS1v15,hashes.SHA256)
        return True
    except InvalidSignature:
        return False

