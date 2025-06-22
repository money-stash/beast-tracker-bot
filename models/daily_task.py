from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    created_date = Column(String)
    daily_task = Column(String)
    is_done = Column(Boolean, default=False)

    user = relationship("User", back_populates="tasks")
