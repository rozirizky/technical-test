from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import settings
from app.redis_client import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(plain: str, hashed: str) -> bool: return pwd_context.verify(plain, hashed)

def _create_token(data: dict, expire_delta: timedelta) -> tuple[str, str]:
    jti = str(uuid4())
    payload = {**data, "jti": jti, "exp": datetime.now(timezone.utc) + expire_delta, "iat": datetime.now(timezone.utc)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM), jti

def create_access_token(user_id: int, role: str) -> str:
    token, _ = _create_token({"sub": str(user_id), "role": role}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return token

def create_refresh_token(user_id: int) -> tuple[str, str]:
    return _create_token({"sub": str(user_id), "type": "refresh"}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token kadaluarsa")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

async def logout_user(access_token: str, user_id: int):
    payload = decode_token(access_token)
    jti = payload.get("jti")
    exp = payload.get("exp")
    if jti and exp:
        ttl = int(exp - datetime.now(timezone.utc).timestamp())
        if ttl > 0:
            await redis_client.blacklist_token(jti, ttl)
    await redis_client.delete_refresh_token(user_id)
