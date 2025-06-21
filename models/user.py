from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    reg_date = Column(String)
    first_name = Column(String)
    username = Column(String)

    tasks = relationship(
        "DailyTask", back_populates="user", cascade="all, delete-orphan"
    )
