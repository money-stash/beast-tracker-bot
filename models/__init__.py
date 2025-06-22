from .user import User
from .daily_task import DailyTask
from .daily_history import DailyHistory
from .weekly_task import WeeklyTask
from sqlalchemy.orm import declarative_base

Base = declarative_base()
