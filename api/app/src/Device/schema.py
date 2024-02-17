from pydantic import validator
from datetime import date
from typing import Optional
from utils.BaseSchema import BaseSchema


class DeviceCreate(BaseSchema):
    user_id: int
    device_name: str
    times_week: int
    daytime: int
    duration: int
    model: str
    brand: str
    effiency: str


class DeviceGet(BaseSchema):
    device_name: str
    times_week: int
    daytime: int
    duration: int
    model: str
    brand: str
    effiency: str

class DeviceUpdate(BaseSchema):
    device_name: Optional[str]
    times_week: Optional[int]
    daytime: Optional[int]
    duration: Optional[int]
    model: Optional[str]
    brand: Optional[str]
    effiency: Optional[str]