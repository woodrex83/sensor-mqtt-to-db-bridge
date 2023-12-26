import asyncio

from loguru import logger
from time import sleep

from src.observers.rmq_subject import RabbitMQSubject
from src.observers.db_observer import PostgresDBObserver
from src.db.database import AsyncDatabase
from src.settings import settings

async def main():
    try:
        db = AsyncDatabase(db=settings.db)
        await db.start()

        rabbitmq_subject = RabbitMQSubject(amqp=settings.amqp)
        db_observer = PostgresDBObserver(db=db)
        
        rabbitmq_subject.attach(db_observer)
        await rabbitmq_subject.start()

    except KeyboardInterrupt:
        logger.info(" [x] AMQP stop consuming now...")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
