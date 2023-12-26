from abc import ABC, abstractmethod
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.lorawan import Lorawan
from src.schemas.lorawan_object import LorawanPayloadInput
from src.utils import convert_keys


class Observer(ABC):
    @abstractmethod
    async def update(self, message):
        pass


class PostgresDBObserver(Observer):
    def __init__(self, db: AsyncSession):
        self._db = db
    
    def __getattr__(self, name):
        private_name = '_' + name
        if private_name in self.__dict__:
            return getattr(self, private_name)
        logger.warning(f" [x] '{type(self).__name__}' object has no attribute '{name}'")
    
    async def update(self, message: LorawanPayloadInput):
        message_dict = message.model_dump()
        record = convert_keys(message_dict)
        result = await Lorawan.create(self.db, record)

        if result:
            # await self.upload_error_output(result)
            logger.error(f" [x] Invalid data : {result}")