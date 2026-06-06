import hashlib
from jose import jwt
import datetime

SECRET_KEY = "mysecretkey123"

# ---------------- PASSWORD HASH ----------------
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- VERIFY PASSWORD ----------------
def verify_password(password: str, hashed: str):
    return hashlib.sha256(password.encode()).hexdigest() == hashed

# ---------------- JWT TOKEN ----------------
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")