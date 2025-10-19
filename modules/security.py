from typing import Dict, Any
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def generate_jwt(payload: Dict[str, Any], secret: str, expires_minutes: int = 15) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = dict(payload)
    to_encode["exp"] = exp
    token = jwt.encode(to_encode, secret, algorithm="HS256")
    return token


def decode_jwt(token: str, secret: str) -> Dict[str, Any]:
    data = jwt.decode(token, secret, algorithms=["HS256"])
    return data


def generate_fernet_key() -> str:
    return Fernet.generate_key().decode("utf-8")


def encrypt_text(text: str, key: str) -> str:
    f = Fernet(key.encode("utf-8"))
    token = f.encrypt(text.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_text(token: str, key: str) -> str:
    f = Fernet(key.encode("utf-8"))
    text = f.decrypt(token.encode("utf-8"))
    return text.decode("utf-8")
