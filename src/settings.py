import tomllib

from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AMQPSettings(BaseModel):
    url: str
    queue_name: str
    queue_arguments: dict
    topic_filter: list[str]


class DatabaseSettings(BaseModel):
    dbhost: str
    port: int
    username: str
    password: str
    db_name: str
    table: str


class Settings(BaseSettings):
    amqp: AMQPSettings
    db: DatabaseSettings


def load_config(path="./config/config.toml") -> Settings:
    try:
        with open(path, "rb") as fb:
            return Settings.model_validate(tomllib.load(fb))
    except FileNotFoundError:
        logger.error(" [x] Missing config.toml")


settings = load_config()
