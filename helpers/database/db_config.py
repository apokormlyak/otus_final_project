import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "BotSynoptic"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:password@postgres/weather_db")
    ASYNC_DATABASE_URL: str = os.getenv(
        "ASYNC_DATABASE_URL", "postgresql+asyncpg://postgres:password@0.0.0.0:5434/postgres"
    )


settings = Settings()