import asyncio
from abc import ABC, abstractmethod

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.lorawan import Lorawan
from src.schemas.lorawan_object import LorawanPayloadInput


class Observer(ABC):
    @abstractmethod
    async def update(self, message):
        pass


class PostgresDBObserver(Observer):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def update(self, message: LorawanPayloadInput):
        record = message.model_dump()
        task = asyncio.create_task(Lorawan.create(self._db._session, record))
        result = await task

        if result:
            # await self.upload_error_output(result)
            logger.error(f" [x] Invalid data : {result}")
