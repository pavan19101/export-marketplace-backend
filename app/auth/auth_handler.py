import time
from typing import Dict, Any
import jwt
from passlib.context import CryptContext
import os

JWT_SECRET = os.getenv("JWT_SECRET", "verysecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def signJWT(user_email: str) -> Dict[str, str]:
    payload = {
        "user_email": user_email,
        "expires": time.time() + 3600 # 1 hour
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

def decodeJWT(token: str) -> Any:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
