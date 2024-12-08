import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DB_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> Session:
    session: Session = async_session()
    try:
        yield session
    finally:
        await asyncio.shield(session.close())
