from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import DatabaseSettings
from src.db.models.lorawan import Base


class AsyncDatabase:
    """Manage asynchronous database sessions using SQLAlchemy"""

    def __init__(self, db: DatabaseSettings):
        self._username = db.username
        self._password = db.password
        self._dbhost = db.dbhost
        self._port = db.port
        self._db_name = db.db_name
        self._engine = None
        self._session = None
        self._async_session = None

    def __setattr__(self, name, value):
        if name in ["username", "password", "dbhost", "port", "db_name"]:
            private_name = "_" + name
            super().__setattr__(private_name, value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        private_name = "_" + name
        if private_name in self.__dict__:
            return getattr(self, private_name)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    async def start(self):
        uri = f"postgresql+asyncpg://{self.username}:{self.password}@{self.dbhost}:{self.port}/{self.db_name}"
        self.engine = create_async_engine(
            uri, echo=False, pool_size=10, max_overflow=100
        )
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        logger.success(" [x] Database Session Created")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.success(" [x] Table created successfully")

    async def __aenter__(self):
        self.session = await self.async_session()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.info(f"An error occurred: {exc_type.__name__}, {exc_val}")
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()

    async def close(self):
        if self.session:
            await self.session.close()
