from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.exception import global_exception_handler, http_exception_handler
from app.api.endpoint import fuel_log, service_schedule, service_history, usage_log
from app.db.base import Base
from app.db.session import engine
from app.models import operational as operational_model  # noqa: F401
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Operational Service - Peminjaman Kendaraan", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fuel_log.router)
app.include_router(service_schedule.router)
app.include_router(service_history.router)
app.include_router(usage_log.router)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get("/")
async def root():
    return {"message": "Operational Service aktif"}
