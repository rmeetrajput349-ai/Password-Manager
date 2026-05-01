import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt(data, password):
    f = Fernet(generate_key(password))
    return f.encrypt(data.encode()).decode()

def decrypt(data, password):
    f = Fernet(generate_key(password))
    return f.decrypt(data.encode()).decode()