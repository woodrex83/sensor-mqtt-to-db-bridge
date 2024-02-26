import json
from uuid import uuid4
from loguru import logger
from pendulum import DateTime
from sqlalchemy import TIMESTAMP, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import JSONB, Insert, insert
from sqlalchemy.dialects.postgresql import UUID as pgUUID 
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from typing import Union, Optional, Any

from src.settings import settings

Base = declarative_base()


class Lorawan(Base):
    __tablename__ = f"{settings.db.table}"

    id: Mapped[pgUUID] = mapped_column(pgUUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    application_id: Mapped[str] = mapped_column(String)
    application_name: Mapped[str] = mapped_column(String)
    device_name: Mapped[str] = mapped_column(String)
    dev_eui: Mapped[str] = mapped_column(String)
    created_time: Mapped[DateTime] = mapped_column(TIMESTAMP(timezone=True))
    rx_info: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    tx_info: Mapped[dict] = mapped_column(JSONB)
    f_cnt: Mapped[int] = mapped_column(Integer)
    f_port: Mapped[int] = mapped_column(Integer)
    data: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    object: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    @classmethod
    async def create(cls, session: AsyncSession, record: dict[str, Any]) -> Union[None, dict]:
        # Convert fields that need JSON encoding
        for field in ["rx_info", "tx_info", "object"]:
            if field in record and record[field] is not None:
                record[field] = json.dumps(record[field])

        result = None
        try:
            # Not using add due to efficiency
            insert_point_stmt: Insert = insert(cls).values(record)
            await session.execute(insert_point_stmt)
            await session.commit()
        except Exception as err:
            await session.rollback()
            logger.warning(err)
            result = {"error": err, "invalid_data": record}

        return result
