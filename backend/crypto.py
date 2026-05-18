import os

from cryptography.fernet import Fernet

_fernet = Fernet(os.environ["CREDENTIAL_ENCRYPTION_KEY"].encode())


def encrypt(plaintext: str) -> bytes:
    return _fernet.encrypt(plaintext.encode())


def decrypt(ciphertext: bytes) -> str:
    return _fernet.decrypt(ciphertext).decode()
