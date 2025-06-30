from models.base import Base
from sqlalchemy import Column, Integer, String


class MiniChallenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer)
    name = Column(String, primary_key=True)
    duration = Column(Integer)
    rules = Column(String)
    action = Column(String)
