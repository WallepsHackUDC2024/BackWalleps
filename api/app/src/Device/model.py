from datetime import date
from sqlalchemy import Column, ForeignKey, String, Integer

from database import Base


class Device(Base):
    __tablename__ = 'device'
    id : int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    device_name: str = Column(String)
    times_week: int = Column(Integer)
    daytime: str = Column(String)
    duration: int = Column(Integer)