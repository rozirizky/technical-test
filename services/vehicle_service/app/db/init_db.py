from app.db.base import Base
from app.db.session import engine
from app.models import vehicle  # noqa: F401 — import agar model terdaftar ke Base  # noqa: F401

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
