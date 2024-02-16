import string
import random
import base64

from error.ValidationException import ValidationException
from src.User.model import User


def get_user_by_mail(db, email):
    return db.query(User).filter(User.email == email).first()


def check_user(db, email, nickname, telephone):
    if get_user_by_mail(db, email) is not None:
        raise ValidationException("Email already exists")


def set_existing_data(db_obj, req_obj):
    data = req_obj.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(db_obj, key, value)
    return list(data.keys())


def isBase64(s):
    return True


def check_image(payload):
    if payload.image is not None:
        if payload.image.startswith("https://") or payload.image.startswith(
                "http://"):
            payload.is_image_url = True
        if not payload.is_image_url:
            if not isBase64(payload.image):
                raise ValidationException("Image is not a valid base64 string")
    return payload


def subtract_lists(list1, list2):
    return [item for item in list1 if item not in list2]