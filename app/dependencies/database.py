from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config_db

# TODO: use env file for DEV, TEST, PROD DB

url = config_db.DB_URL.get_secret_value()
engine = create_async_engine(url=url, echo=True)

SessionFactory = async_sessionmaker(engine, autoflush=False)


async def get_session():
    session: AsyncSession = SessionFactory()
    try:
        yield session
    finally:
        session.aclose()
