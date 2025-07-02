from models.base import Base
from sqlalchemy import Column, Integer


class LeadBord(Base):
    __tablename__ = "leaderbord"

    user_id = Column(Integer, primary_key=True)
    streak = Column(Integer)
