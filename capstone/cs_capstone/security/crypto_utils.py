from cryptography.fernet import Fernet
import hashlib


def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)


def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_hash(data: bytes, expected_hex: str) -> bool:
    return sha256_hash(data) == expected_hex
