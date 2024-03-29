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
    is_sections: bool = Column(Boolean, default=True)
    home_hours: int = Column(Integer, default=0)
    home_duration: int = Column(Integer, default=1)
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }
    class Config:
        orm_mode = True