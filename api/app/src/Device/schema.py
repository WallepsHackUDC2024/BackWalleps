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
    efficiency: str

    @validator('daytime')
    def daytime_validation(cls, v):
        if (v < 0 or v > 23):
            raise ValueError(
                'value must be between 0 and 23'
            )
        return v
    
    @validator('duration')
    def duration_validation(cls, v):
        if (v < 0 or v > 24):
            raise ValueError(
                'value must be between 0 and 24'
            )
        return v
    
    @validator('times_week')
    def times_week_validation(cls, v):
        if (v < 0 or v > 7):
            raise ValueError(
                'value must be between 0 and 7'
            )
        return v

class DeviceGet(BaseSchema):
    id: int
    device_name: str
    times_week: int
    daytime: int
    duration: int
    model: str
    brand: str
    efficiency: str

class DeviceUpdate(BaseSchema):
    device_name: Optional[str]
    times_week: Optional[int]
    daytime: Optional[int]
    duration: Optional[int]
    model: Optional[str]
    brand: Optional[str]
    efficiency: Optional[str]