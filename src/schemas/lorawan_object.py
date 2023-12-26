from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    applicationID: str
    applicationName: str
    deviceName: str
    devEUI: str
    createdTime: Optional[datetime]
    rxInfo: list[RxInfo]
    txInfo: TxInfo
    fCnt: int
    fPort: int
    data: str
    object: dict
