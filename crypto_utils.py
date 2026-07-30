import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Uses PBKDF2 to stretch the weak master password into an 
    un-guessable 256-bit key. Runs 600,000 iterations to stop brute-forcing.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # 32 bytes = 256 bits
        salt=salt,
        iterations=600000,  
    )
    return kdf.derive(master_password.encode())

def encrypt_data(key: bytes, plaintext: str) -> bytes:
    """
    Encrypts the text using AES-256-GCM. 
    Appends a unique 12-byte nonce to the front of the ciphertext.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # Unique initialization vector per password
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext

def decrypt_data(key: bytes, encrypted_blob: bytes) -> str:
    """
    Extracts the nonce and decrypts the ciphertext back into plain text.
    Throws an error if the key is wrong or data was tampered with.
    """
    aesgcm = AESGCM(key)
    nonce = encrypted_blob[:12]
    ciphertext = encrypted_blob[12:]
    try:
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_bytes.decode()
    except Exception:
        raise ValueError("Decryption failed. Bad key or corrupted vault.")