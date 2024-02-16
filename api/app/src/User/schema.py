from pydantic import validator
from datetime import date
from typing import Optional
import re
from utils.BaseSchema import BaseSchema


class UserCreate(BaseSchema):
    name: str
    surname: str
    password: str
    email: str
    image: Optional[str]
    is_image_url: Optional[bool]

    @validator('email')
    def email_validation(cls, v):
        if (re.search(
                "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
                v) is None):
            raise ValueError('must be a valid email')
        return v


    @validator('password')
    def password_validation(cls, v):
        if (re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$", v)
                is None):
            raise ValueError(
                'must contain at least 8 characters, at least one uppercase letter, one lowercase letter and one number'
            )
        return v


class UserGet(BaseSchema):
    name: str
    surname: str
    email: str
    image: Optional[str]
    is_image_url: Optional[bool]

class UserGetAll(UserGet):
    password: str

class UserUpdate(BaseSchema):
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    email: Optional[str]
    image: Optional[str]
    is_image_url: Optional[bool]