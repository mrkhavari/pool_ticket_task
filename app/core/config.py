from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Pool Ticket Task"
    APP_VERSION: str = "0.1.0"
    DB_URL: str = "postgresql+asyncpg://db_user:db_password@postgres:5432/db"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    USER_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://redis:6379"
    ENABLE_USING_CACHE: bool = True
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
