from datetime import datetime as date
from sqlalchemy.orm import Session

from security import get_password_hash
from utils.service_utils import set_existing_data, check_image

from error.NotFoundException import NotFoundException

from utils.hide_utils import user_show_private
from utils.service_utils import check_user

from src.User.model import User as ModelUser
from src.Device.model import Device as ModelDevice

from src.User.schema import UserGet as UserCreateSchema
from src.User.schema import UserUpdate as UserUpdateSchema


import predictor.solver as solver


def get_all(db: Session):
    return db.query(ModelUser).all()


def get_user(userId: int, db: Session):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if user is None:
        raise NotFoundException("User not found")
    user_show_private(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(ModelUser).filter(ModelUser.email == email).first()
    if user is None:
        raise NotFoundException("User not found")
    return user


def add_user(payload: UserCreateSchema, db: Session):
    check_user(db, payload.email)
    new_user = ModelUser(**payload.dict())
    if payload.image is not None:
        payload = check_image(payload)
    new_user.password = get_password_hash(payload.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def remove_user(userId: int, db: Session):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if not user:
        raise NotFoundException("User not found")
    db.delete(user)
    db.commit()
    return user


def update_user(userId: int, payload: UserUpdateSchema,
                        db: Session):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if user is None:
        raise NotFoundException("User not found")
    if payload.image is not None:
        payload = check_image(payload)
    updated = set_existing_data(user, payload)
    user.updated_at = date.now()
    updated.append("updated_at")
    if payload.password is not None:
        user.password = get_password_hash(payload.password)
    db.commit()
    db.refresh(user)
    return user, updated


def get_scheduler(userId: int, db: Session):
    user = db.query(ModelUser).filter(ModelUser.id == userId).first()
    if user is None:
        raise NotFoundException("User not found")
    devices = db.query(ModelDevice).filter(ModelDevice.user_id == userId).all()
    solution = solver.solve(devices, user)
    return solution