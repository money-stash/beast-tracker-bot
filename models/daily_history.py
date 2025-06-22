from models.base import Base
from sqlalchemy import Column, Integer, String, Boolean


class DailyHistory(Base):
    __tablename__ = "daily_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    task_id = Column(Integer)
    date = Column(String)
    is_done = Column(Boolean)
