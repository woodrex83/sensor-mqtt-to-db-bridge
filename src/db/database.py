from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.models.lorawan import Base
from src.settings import DatabaseSettings


class AsyncDatabase:
    """Manage asynchronous database sessions using SQLAlchemy"""

    def __init__(self, db: DatabaseSettings):
        self._username: str = db.username
        self._password: str = db.password
        self._dbhost: int = db.dbhost
        self._port: str = db.port
        self._db_name: str = db.db_name

        uri = f"postgresql+asyncpg://{self._username}:{self._password}@{self._dbhost}:{self._port}/{self._db_name}"
        self._engine = create_async_engine(uri, echo=False, pool_size=10, max_overflow=100)
        self._sessionmaker = async_sessionmaker(
            self._engine, expire_on_commit=True, class_=AsyncSession
        )
        self._session: AsyncSession = self._sessionmaker()
        logger.success(" [x] Database Session Created")

    async def start(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.success(" [x] Table created successfully")
