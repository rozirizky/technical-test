from app.db.base import Base
from app.db.session import engine
from app.models import user  # noqa: F401 - registers models to Base.metadata

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
