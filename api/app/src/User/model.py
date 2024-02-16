from datetime import date
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from database import Base
from sqlalchemy.orm import deferred

from sqlalchemy.orm import Mapped


class User(Base):
    __tablename__ = 'user'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    surname: str = Column(String)
    password: Mapped[str] = deferred(Column(String))
    email: Mapped[str] = deferred(Column(String, unique=True, index=True))
    type: str = Column(String)
    created_at: date = Column(DateTime, default=date.today())
    updated_at: date = Column(DateTime, default=date.today())
    image: str = Column(String, default="")
    is_image_url: bool = Column(Boolean, default=False)
    contract_type: str = Column(String, default="")
    power: int = Column(Integer, default=0)
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }
    class Config:
        orm_mode = True