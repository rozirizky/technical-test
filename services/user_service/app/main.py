from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.exception import global_exception_handler, http_exception_handler
from app.api.endpoint import user, location, role, auth
from app.db.base import Base
from app.db.session import engine
from app.models import user as user_model  # noqa: F401 - registers models
from contextlib import asynccontextmanager
import sys, os
from config import settings
from app.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await redis_client.disconnect()
    await engine.dispose()


app = FastAPI(title="User Service - Peminjaman Kendaraan", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(location.router)
app.include_router(user.router)
app.include_router(role.router)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get("/")
async def root():
    return {"message": "User Service aktif"}
