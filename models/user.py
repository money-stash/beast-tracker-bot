from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, Boolean


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    reg_date = Column(String)
    first_name = Column(String)
    username = Column(String)
    health_balance = Column(Float, default=0)
    is_baned = Column(Boolean, default=False)
    dme_top = Column(Integer, default=0)
    partner_id = Column(Integer, default=0)

    tasks = relationship(
        "DailyTask", back_populates="user", cascade="all, delete-orphan"
    )
