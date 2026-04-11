from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SERVICE_NAME: str = "booking-service"
    DEBUG: bool = False
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/2"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    USER_SERVICE_URL: str = "http://user-service:8000"
    VEHICLE_SERVICE_URL: str = "http://vehicle-service:8000"
    APPROVAL_LEVELS: int = 2
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings: return Settings()
settings = get_settings()
