from models.base import Base
from sqlalchemy import Column, Integer, String


class ScheduleMessage(Base):
    __tablename__ = "scheduled_msgs"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    media_path = Column(String)
    date = Column(String)
    time = Column(String)
    repeat = Column(String)
