from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config_db
from app.models.base import BaseModel
from app.models.user import User

print(User)

# TODO: use env file for DEV, TEST, PROD DB

url = config_db.DB_URL.get_secret_value()
engine = create_async_engine(url=url, echo=True)

SessionFactory = async_sessionmaker(engine, autoflush=False)


async def create_tables():
    async with engine.connect() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)
        await connection.commit()
        await connection.aclose()


def delete_tables():
    BaseModel.metadata.drop_all(engine)


async def get_session():
    session: AsyncSession = SessionFactory()
    try:
        yield session
    finally:
        session.aclose()
