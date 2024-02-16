from pydantic import validator
from datetime import date
from typing import Optional
from utils.BaseSchema import BaseSchema


class DeviceCreate(BaseSchema):
    user_id: int
    device_name: str
    times_week: int
    daytime: str
    duration: int


class DeviceGet(BaseSchema):
    name: str
    surname: str
    email: str
    image: Optional[str]
    is_image_url: Optional[bool]

class DeviceGetAll(DeviceGet):
    id: int
    device_name: str
    times_week: int
    daytime: str
    duration: int

class DeviceUpdate(BaseSchema):
    device_name: Optional[str]
    times_week: Optional[int]
    daytime: Optional[str]
    email: Optional[str]
    duration: Optional[int]