from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RxInfo(BaseModel):
    mac: str
    rssi: int
    loRaSNR: float
    name: str
    latitude: float
    longitude: float
    altitude: float


class DataRate(BaseModel):
    modulation: str
    bandwidth: int
    spreadFactor: int


class TxInfo(BaseModel):
    frequency: int
    dataRate: DataRate
    adr: bool
    codeRate: str


class LorawanPayloadInput(BaseModel):
    application_id: str = Field(alias="applicationID")
    application_name: str = Field(alias="applicationName")
    device_name: str = Field(alias="deviceName")
    dev_eui: str = Field(alias="devEUI")
    created_time: Optional[datetime] = Field(alias="createdTime")
    rx_info: list[RxInfo] = Field(alias="rxInfo")
    tx_info: TxInfo = Field(alias="txInfo")
    f_cnt: int = Field(alias="fCnt")
    f_port: int = Field(alias="fPort")
    data: str
    object: dict
