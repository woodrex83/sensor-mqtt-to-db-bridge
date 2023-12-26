import asyncio
import pendulum
import orjson

from aio_pika import IncomingMessage, connect_robust, exceptions
from abc import ABC
from loguru import logger

from src.schemas.lorawan_object import LorawanPayloadInput
from src.settings import AMQPSettings


class Subject(ABC):
    def __init__(self):
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    async def notify(self, message):
        for observer in self.observers:
            await observer.update(message)


class RabbitMQSubject(Subject):
    def __init__(self, amqp: AMQPSettings):
        super().__init__()
        self._url = amqp.url
        self._queue_name = amqp.queue_name
        self._queue_args = amqp.queue_arguments
        self._topic_filter = amqp.topic_filter
        self._channel = None
        self._connection = None
    
    def __setattr__(self, name, value):
        if name in ['url', 'queue_name', 'queue_args', 'topic_filter', 'channel', 'connection']:
            private_name = '_' + name
            super().__setattr__(private_name, value)
        else:
            super().__setattr__(name, value)
    
    def __getattr__(self, name):
        private_name = '_' + name
        if private_name in self.__dict__:
            return getattr(self, private_name)
        logger.warning(f" [x] '{type(self).__name__}' object has no attribute '{name}'")
    
    async def start(self):
        while True:
            try:
                self.connection = await connect_robust(self._url)
                
                async with self.connection:
                    self.channel = await self.connection.channel()
                    queue = await self.channel.declare_queue(
                        name=self.queue_name,
                        durable=True,
                        arguments=self.queue_args
                    )
                    await queue.consume(self.process_message)

                    logger.success(" [x] Waiting for messages. To exit press CTRL+C")
                    await asyncio.Future()
            except exceptions.AMQPConnectionError:
                logger.warning(" [x] Connection fail, retrying in 1 second.")
                await asyncio.sleep(1)
            except KeyboardInterrupt: 
                logger.info(" [x] Received keyboard interrupt...")
            except Exception as err:
                logger.error(f" [x] An error occurred: {err}")
            finally:
                await self.connection.close()

    async def process_message(
        self,
        message: IncomingMessage
    ):
        # Check topic
        topic = message.routing_key.replace(".", "/")
        now = pendulum.now()
        accept_topics = self.topic_filter

        if (topic in accept_topics) and message.body_size:
            logger.debug(f" [x] Received message on topic '{topic}'")
            raw_payload = message.body.decode("utf-8")
            json_payload = orjson.loads(raw_payload)
            json_payload["createdTime"] = now

            try:
                lora_payload = LorawanPayloadInput.model_validate(json_payload)
                logger.success(lora_payload)
                await self.notify(lora_payload)

            except ValueError as err:
                # self.upload_error_output(err)
                logger.error(f" [x] Invalid raw data received from AMQP: {err}")