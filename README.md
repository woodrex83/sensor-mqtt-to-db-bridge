![](https://img.shields.io/badge/python-%203.11%20-blue) ![](https://img.shields.io/badge/paho_mqtt-1.6.1-blue) ![](https://img.shields.io/badge/pika-1.3.2-blue) ![](https://img.shields.io/badge/confluent_kafka-2.3.0-blue)
# sensor-mqtt-to-db-bridge
A bridging connector designed to facilitate the transfer of data from Lorawan IoT sensors utilizing MQTT/AMQP to a database.


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

-   Create record in postgres db


## Config
Rename **config.toml.example** to **config.toml**
```
[mqtt]
broker_address = "<your_endpoint>"
broker_port = 1883
topic = "+/+/+/#"

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
- MQTT Broker
    ```
    docker run -it -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto:2.0.18
    ```
    mosquitto.conf
    ```
    listener 1883
    allow_anonymous true
    ```

- Postgres
    ```
    docker run -it --name test-pg -p 5500:5432 -e POSTGRES_PASSWORD=postgres -d postgres:15-alpine
    ```
    
### Result



