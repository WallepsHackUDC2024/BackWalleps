from datetime import datetime as date
from sqlalchemy.orm import Session

from security import get_password_hash
from utils.service_utils import set_existing_data

from error.NotFoundException import NotFoundException

from src.Device.model import Device as ModelDevice

from src.Device.schema import DeviceGet as DeviceCreateSchema
from src.Device.schema import DeviceUpdate as DeviceUpdateSchema


def get_all(db: Session):
    return db.query(ModelDevice).all()


def get_device(deviceId: int, db: Session):
    device = db.query(ModelDevice).filter(ModelDevice.id == deviceId).first()
    if device is None:
        raise NotFoundException("Device not found")
    return device


def get_device_by_id(userId: int, db: Session):
    device = db.query(ModelDevice).filter(ModelDevice.user_id == userId).all()
    if device is None:
        raise NotFoundException("No devices found for this user")
    return device


def add_device(payload: DeviceCreateSchema, db: Session):
    new_device = ModelDevice(**payload.dict())

    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def remove_device(deviceId: int, db: Session):
    device = db.query(ModelDevice).filter(ModelDevice.id == deviceId).first()
    if not device:
        raise NotFoundException("Device not found")
    db.delete(device)
    db.commit()
    return device


def update_device(deviceId: int, payload: DeviceUpdateSchema,
                        db: Session):
    device = db.query(ModelDevice).filter(ModelDevice.id == deviceId).first()
    if device is None:
        raise NotFoundException("Device not found")
    updated = set_existing_data(device, payload)
    device.updated_at = date.now()
    updated.append("updated_at")
    if payload.password is not None:
        device.password = get_password_hash(payload.password)
    db.commit()
    db.refresh(device)
    return device, updated
