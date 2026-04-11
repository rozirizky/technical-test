from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schema.user import LoginRequest, TokenResponse, RefreshRequest
from app.service.auth import create_access_token , verify_password ,create_refresh_token ,decode_token ,logout_user
from app.service.users import get_user_by_id , get_user_by_email
from app.redis_client import redis_client

router = APIRouter(prefix="/api/auth", tags=["auth"])
bearer = HTTPBearer()

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    access_token = create_access_token(user.id, user.role.name)
    refresh_token, jti = create_refresh_token(user.id)
    await redis_client.set_refresh_token(user.id, jti)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Bukan refresh token")
    user_id = int(payload["sub"])
    if await redis_client.get_refresh_token(user_id) != payload.get("jti"):
        raise HTTPException(status_code=401, detail="Refresh token tidak valid")
    user = await get_user_by_id(db, user_id)
    access_token = create_access_token(user.id, user.role.name)
    new_refresh, new_jti = create_refresh_token(user.id)
    await redis_client.set_refresh_token(user.id, new_jti)
    return TokenResponse(access_token=access_token, refresh_token=new_refresh)

@router.post("/logout", status_code=204)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    payload = decode_token(credentials.credentials)
    await logout_user(credentials.credentials, int(payload["sub"]))
