import asyncio
from abc import ABC

import orjson
import pendulum
from aiomqtt import Client as MQTTClient
from aiomqtt import Message, MqttError
from loguru import logger

from src.schemas.lorawan_object import LorawanPayloadInput
from src.settings import MQTTSettings


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


class MQTTSubject(Subject):
    def __init__(self, mq: MQTTSettings):
        super().__init__()
        self._host = mq.host
        self._port = mq.port
        self._topic_filter = mq.topic_filter
        self._username = mq.username
        self._password = mq.password
        self._client = None

    async def start(self):
        while True:
            try:
                self._client = MQTTClient(
                    hostname=self._host,
                    port=self._port,
                    username=self._username,
                    password=self._password,
                    max_concurrent_outgoing_calls=100,
                )

                async with self._client as client:
                    for topic in self._topic_filter:
                        await client.subscribe(topic)

                    logger.success(" [x] Waiting for messages. To exit press CTRL+C")
                    async with client.messages() as messages:
                        async for message in messages:
                            await self.process_message(message)
                            # await asyncio.Future()

            except MqttError as mqtt_err:
                logger.warning(f" [x] MQTT error occurred: {mqtt_err}, retrying in 1 second.")
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info(" [x] Received keyboard interrupt...")
            except Exception as err:
                logger.error(f" [x] An error occurred: {err}")

    async def process_message(self, message: Message):
        topic = str(message.topic)
        now = pendulum.now()
        json_payload = orjson.loads(message.payload)
        json_payload["createdTime"] = now
        logger.debug(f" [x] Received message on topic '{topic}'")

        try:
            lora_payload = LorawanPayloadInput.model_validate(json_payload)
            logger.success(lora_payload)
            await self.notify(lora_payload)

        except ValueError as err:
            # self.upload_error_output(err)
            logger.error(f" [x] Invalid raw data received from MQTT: {err}")
