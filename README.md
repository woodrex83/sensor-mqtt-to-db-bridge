![](https://img.shields.io/badge/python-%203.11%20|%203.12%20-blue) ![](https://img.shields.io/badge/aiomqtt-1.2.1-blue) ![](https://img.shields.io/badge/aio_pika-9.3.1-blue)
# sensor-mqtt-to-db-bridge
A bridging connector designed to facilitate the transfer of data from ChirpStack utilizing MQTT/AMQP to a database.


## Structure

*Rabbit MQ version is released in **amqp** branch.

(horizontal flow chart)
(Whole system with circle)

## Feature

-   Consumer topic filter
	+ Support wildcard topic (MQTT only)

-   Consumer protocol version
    + Support v3.1/3.1.1 in AMQP
    + Support v3.1/3.1.1/5 in MQTT

-   Create record in Postgres


## Config
Rename **config.toml.example** to **config.toml**
```
[amqp]
url = "amqp://guest:guest@localhost:5672"
queue_name = "lorawan"
queue_arguments = {"x-message-ttl" = 10800000}
topic_filter = [
    "application/APPLICATION_ID/device/DEV_EUI_A/event/up",
    "application/APPLICATION_ID/device/DEV_EUI_B/event/up"
]

[db]
dbhost = "localhost"
port = 5500
username = "postgres"
password = "postgres"
db_name = "iot"
table = "lorawan_raw_data"
```


## Performance
### Test Environment
**DO NOT use the following setting in production environment !!**
- Postgres
    ```
    docker run -it --name test-pg -p 5500:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=iot -d postgres:15-alpine
    ```
    
### Result



