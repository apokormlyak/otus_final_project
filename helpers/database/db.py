from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, registry, sessionmaker

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "BotSynoptic"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:password@postgres/test_db")
    ASYNC_DATABASE_URL: str = os.getenv(
        "ASYNC_DATABASE_URL", "postgresql+asyncpg://admin:password@postgres/test_db"
    )


settings = Settings()

async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

mapper_registry = registry()
Base: DeclarativeMeta = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
