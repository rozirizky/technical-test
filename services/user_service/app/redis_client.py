import redis.asyncio as redis
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import settings

class RedisClient:
    def __init__(self): self.client = None
    async def connect(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    async def disconnect(self):
        if self.client: await self.client.aclose()
    async def set_refresh_token(self, user_id: int, jti: str):
        await self.client.setex(f"refresh:{user_id}", settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, jti)
    async def get_refresh_token(self, user_id: int) -> str | None:
        return await self.client.get(f"refresh:{user_id}")
    async def delete_refresh_token(self, user_id: int):
        await self.client.delete(f"refresh:{user_id}")
    async def blacklist_token(self, jti: str, ttl: int):
        await self.client.setex(f"blacklist:{jti}", ttl, "1")
    async def is_blacklisted(self, jti: str) -> bool:
        return await self.client.exists(f"blacklist:{jti}") == 1
    async def cache_user(self, user_id: int, data: str, ttl: int = 300):
        await self.client.setex(f"user:{user_id}", ttl, data)
    async def get_cached_user(self, user_id: int) -> str | None:
        return await self.client.get(f"user:{user_id}")
    async def invalidate_user_cache(self, user_id: int):
        await self.client.delete(f"user:{user_id}")

redis_client = RedisClient()
