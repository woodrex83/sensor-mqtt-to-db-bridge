import asyncio

from loguru import logger

from src.observers.mqtt_subject import MQTTSubject
from src.observers.db_observer import PostgresDBObserver
from src.db.database import AsyncDatabase
from src.settings import settings

async def main():
    try:
        db = AsyncDatabase(db=settings.db)
        await db.start()

        mqtt_subject = MQTTSubject(mq=settings.mqtt)
        db_observer = PostgresDBObserver(db=db)
        
        mqtt_subject.attach(db_observer)
        await mqtt_subject.start()

    except KeyboardInterrupt:
        logger.info(" [x] MQTT stop consuming now...")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
