import json

from loguru import logger
from uuid import uuid4
from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import declarative_base
from typing import Union

from src.schemas.lorawan_object import LorawanPayloadInput
from src.settings import settings

Base = declarative_base()


class Lorawan(Base):
    __tablename__ = f"{settings.db.table}"

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(String)
    application_name = Column(String)
    device_name = Column(String)
    dev_eui = Column(String)
    created_time = Column(TIMESTAMP(timezone=True))
    rx_info = Column(JSONB, nullable=True)
    tx_info = Column(JSONB)
    f_cnt = Column(Integer)
    f_port = Column(Integer)
    data = Column(String, nullable=True)
    object = Column(JSONB, nullable=True)

    @classmethod
    async def create(cls, db, record: dict) -> Union[None, dict]:
        # Convert fields that need JSON encoding
        for field in ["rx_info", "tx_info", "object"]:
            if field in record and record[field] is not None:
                record[field] = json.dumps(record[field])

        async with db.async_session() as session:
            result = None
            try:
                # Not using add due to efficiency
                insert_point_stmt = insert(cls).values(record)
                await session.execute(insert_point_stmt)
                await session.commit()
            except Exception as err:
                await session.rollback()
                logger.warning(err)
                result = {"error": err, "invalid_data": record}

            return result
