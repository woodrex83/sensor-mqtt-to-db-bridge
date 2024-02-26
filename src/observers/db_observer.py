import asyncio
from asyncio import Task
from abc import ABC, abstractmethod
from loguru import logger
from typing import Any
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

    async def update(self, message: LorawanPayloadInput) -> None:
        record: dict[str, Any] = message.model_dump()
        task: Task = asyncio.create_task(Lorawan.create(self._db._session, record))
        result: Any = await task

        if isinstance(result, dict):
            # await self.upload_error_output(result)
            logger.error(f" [x] Invalid data : {result}")
