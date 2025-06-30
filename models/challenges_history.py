from models.base import Base
from sqlalchemy import Column, Integer, String, Boolean


class ChallengeHistory(Base):
    __tablename__ = "challenges_history"

    id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer)
    date = Column(String)
    user_id = Column(Integer)
    is_executed = Column(Boolean, default=False)
