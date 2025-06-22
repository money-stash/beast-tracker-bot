from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class WeeklyTask(Base):
    __tablename__ = "weekly_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    weekly_task = Column(String)
    is_done = Column(Boolean, default=False)

    # user = relationship("User", back_populates="tasks")
