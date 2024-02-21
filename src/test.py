import asyncio

import orjson
import pendulum

from src.db.database import AsyncDatabase
from src.observers.db_observer import PostgresDBObserver
from src.schemas.lorawan_object import LorawanPayloadInput
from src.settings import settings

message = """{
    "applicationID":"1",
    "applicationName":"test_ds18b20",
    "deviceName":"arduino_uno",
    "devEUI":"1234567890123456",
    "rxInfo":[
        {
            "mac":"aa755a0048050130",
            "rssi":-57,
            "loRaSNR":10,
            "name":"raspberry_pi",
            "latitude":48.466860686785175,
            "longitude":1.019478797912605,
            "altitude":0
        }
    ],
    "txInfo":{
        "frequency":868100000,
        "dataRate":{
            "modulation":"LORA",
            "bandwidth":125,
            "spreadFactor":7
        },
        "adr":true,
        "codeRate":"4/5"
    },
    "fCnt":9,
    "fPort":1,
    "data":"Z29vZGJ5ZQ==",
    "object":{
        
    }
}"""


async def main():
    json_payload = orjson.loads(message)
    now = pendulum.now()
    json_payload["createdTime"] = now
    lora_payload = LorawanPayloadInput.model_validate(json_payload)

    db = AsyncDatabase(db=settings.db)
    await db.start()
    db_observer = PostgresDBObserver(db=db)
    for _ in range(1000):
        await db_observer.update(lora_payload)


if __name__ == "__main__":
    asyncio.run(main())
