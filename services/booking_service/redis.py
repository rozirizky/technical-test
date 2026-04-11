import redis.asyncio as redis
from app.config import settings

class RedisClient:
    def __init__(self):
        self.client: redis.Redis | None = None

    async def connect(self):
        self.client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
        await self.client.ping()

    async def disconnect(self):
        if self.client:
            await self.client.aclose()

    def _check(self):
        if not self.client:
            raise RuntimeError("Redis not connected")

    async def set(self, key: str, value: str, ttl: int = 300):
        self._check()
        await self.client.setex(key, ttl, value)

    async def get(self, key: str):
        self._check()
        return await self.client.get(key)

    async def delete(self, key: str):
        self._check()
        await self.client.delete(key)


redis_client = RedisClient()