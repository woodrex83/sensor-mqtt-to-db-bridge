import asyncio

from loguru import logger

from src.db.database import AsyncDatabase
from src.observers.db_observer import PostgresDBObserver
from src.observers.mqtt_subject import MQTTSubject
from src.settings import settings
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def main() -> None:
    try:
        db = AsyncDatabase(db=settings.db)
        mqtt_subject = MQTTSubject(mq=settings.mqtt)
        db_observer = PostgresDBObserver(db=db)

        mqtt_subject.attach(db_observer)
        await mqtt_subject.start()

    except KeyboardInterrupt:
        logger.info(" [x] MQTT stop consuming now...")


if __name__ == "__main__":
    asyncio.run(main())
