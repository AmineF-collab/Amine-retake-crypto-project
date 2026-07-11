""" textbook rsa bonus :
Ce fichier n'est pas utilisé dans le projet il est seulement utilisé pour montrer la compréhension de la génération de clés RSA, 
du hashing, de la signature et de la verification de la signature. Le projet utilise la librairie cryptography et hashlib.

Limitation : je n'ai pas trouvé comment générer de grands nombres premiers aléatoires. Néanmoins dans ce contexte la donnée 
précise que ce projet ne se soucie pas de la confidentialité car on protège contre la falsification, pas contre l'espionnage. C'est 
justement pour cette raison que le workflow principal du projet utilise la librairie cryptography, avec de vraies 
clés 2048 bits."""
import hashlib

def verify_prime(p):
    if(p<2):
        return False
    for petit_nombre_premier in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        if p == petit_nombre_premier: # Si c'est un petit nombre premier on renvoie true
            return True
        if p % petit_nombre_premier == 0: # Si il est divisible sans reste par un petit nombre premier il n'est pas premier donc False
            return False

"""Maintenant qu'on a notre nombre premier on peut commencer a créer les clés"""

"""Pour trouver l'exponent publique de la clé publique il faut qu'il soit un nombre premier et qu'il ne soit pas égale a phi"""
def generate_public_exponent(phi):
    for public_exponent in range(2, phi):
        if verify_prime(public_exponent) and phi % public_exponent != 0:
            return public_exponent
    raise ValueError("Aucun e valide trouvé")

"""Pour trouver d de la clé privé il faut trouver un nombre telle que (d * e) % phi = 1 appelée l'inverse modulaire de e modulo phi"""
def generate_inverse_modulaire(e,phi):
    d=0
    while(d*e)%phi != 1:
        d += 1
    return d

"""Créons maintenant les deux clé avec l'exponent publique et l'inverse modulaire de celui ci modulo phi """
def generate_keys(p,q):
    if verify_prime(p) and verify_prime(q):
        n = p * q
        phi = (p-1)*(q-1)
        e = generate_public_exponent(phi)  
        d = generate_inverse_modulaire(e,phi)
        public_key = (e,n)
        private_key = (d,n)
        return public_key, private_key
    else:
        raise ValueError("p et q doivent être des nombres premiers")

"""L'encryption et la decryption des messages sont le cours mais n'est pas demandé dans le projet car le projet ne tient pas en compte la 
confidentialité cependant je les fait quand même"""

"""L'encryption du message se fait avec cette formule Cipher = Message^E % N"""
def encrypt(message, public_key):
    e, n = public_key
    return (pow(message, e)%n)
"""Pour la décryption c'est cette formule Cipher^D % N = Message"""
def decrypt(cipher, private_key):
    d, n = private_key
    return pow(cipher,d) % n
"""Le hash est le résultat d'une fonction mathématique qui prend n'importe quelle donnée, la découpe en blocs de 512 bits 
(avec du remplissage sur le dernier bloc si besoin), puis fait beaucoup d'opérations comme des AND, OR, XOR, ou encore des 
rotations de bits sur chaque bloc. Cela renvoie une chaîne de taille fixe de 256 bits,un meme message renvoie toujours le 
meme hash et il est impossible de le retrouver a partir du hash c'est ce qui vas nous aider à vérifier la signature"""
def hash_message(message: bytes, n: int) -> int:
    digest = hashlib.sha256(message).digest()
    return int.from_bytes(digest, byteorder="big") % n
"""La signature correspond au message hashé encrypter avec la clé privé soit Signature = (Message_hashé^D) % N"""
def sign(message: bytes, private_key):
    d, n = private_key
    h = hash_message(message, n)
    return encrypt(h,(d,n))
"""La vérification quand a elle conciste a décodé le message signé pour retrouver le hash car comme dit plus haut 
un message hashé renvoie toujours le meme hash donc si le hash est différent la signature est fausse : soit la clé publique est pas la bonne,
soit la signature a été modifié ou corrompue soit le message a été modifié ou corrompue"""
def verify(message: bytes, signature: int, public_key):
    e, n = public_key
    h = hash_message(message, n)
    if decrypt(signature,(e,n)) != h:
        return False
    return True
"""Cette fonction prouve l'intégrité du message car si il est modifé ça renvoie faux mais aussi l'autentification de l'origine car seule
cette clé privé peut signer le message qui se verifira avec sa clé publique"""

print("Test Textbook RSA\n")
p = 7
q = 19
public_key, private_key = generate_keys(p,q)
e = public_key[0]
n = public_key[1]
d = private_key[0]
print(f"Primes P,Q : {p}, {q}")
print(f"Semiprime N : {n}")
print(f"Public_key (E,N): {public_key}")
print(f"Private_key (D,N): {private_key}\n")

message = 60 
cipher = encrypt(message,public_key)
message_decrypted = decrypt(cipher, private_key)
print(f"Message : {message}")
print(f"Cipher : {cipher}")
print(f"Decrypted message : {message_decrypted}\n")

text = b"je suis un text encode en binaire"
sig = sign(text, private_key)
print(f"Message: {text}")
print(f"Signature: {sig}")
print(f"Verification le message est: {verify(text, sig, public_key)}\n")

corrupted = b"je suis un message tres corrompue"
print(f"Message corrompue : {corrupted}")
print(f"Verification le message est: {verify(corrupted, sig, public_key)}\n")