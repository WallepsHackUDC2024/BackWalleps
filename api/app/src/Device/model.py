from datetime import date
from sqlalchemy import Column, ForeignKey, String, Integer

from database import Base


class Device(Base):
    __tablename__ = 'device'
    id: int = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), primary_key=True)
    device_name: str = Column(String)
    times_week: int = Column(Integer)
    daytime: str = Column(String)
    duration: int = Column(Integer)