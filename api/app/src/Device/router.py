from typing import List, Union
from fastapi import Depends, Response, APIRouter
from sqlalchemy.orm import Session

from database import get_db


import src.Device.service as device_service

from src.Device.model import Device as ModelDevice


from src.Device.schema import DeviceGet as DeviceGetSchema
from src.Device.schema import DeviceCreate as DeviceCreateSchema
from src.Device.schema import DeviceUpdate as DeviceUpdateSchema

router = APIRouter(
    prefix="/device",
    tags=["Device"],
)


@router.post("/")
def signup(payload: DeviceCreateSchema,
                 db: Session = Depends(get_db)):
    new_device = device_service.add_device(payload, db)
    return {
        "success": True,
        "device_id": new_device.id,
    }


@router.get("/all", response_model=List[DeviceGetSchema])
def get_devices(db: Session = Depends(get_db)):
    return device_service.get_all(db)


@router.get("/{deviceId}", response_model=DeviceGetSchema)
def get_device(deviceId: int,
                     db: Session = Depends(get_db)):
    return device_service.get_device(deviceId, db)


@router.get("/user/{userId}", response_model=List[DeviceGetSchema])
def get_device(userId: int,
                     db: Session = Depends(get_db)):
    return device_service.get_device_by_userId(userId, db)


@router.put("/{deviceId}")
def update_device(deviceId: int,
                        payload: DeviceUpdateSchema,
                        db: Session = Depends(get_db)):
    device, updated = device_service.update_device(
        deviceId, payload, db)
    return {"success": True, "updated_id": device.id, "updated": updated}


@router.delete("/{deviceId}")
def delete_device(deviceId: int,
                        db: Session = Depends(get_db)):
    device = device_service.remove_device(deviceId, db)
    return {"success": True, "deleted_id": device.id}

