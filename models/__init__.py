from .user import User
from .daily_task import DailyTask
from .daily_history import DailyHistory
from .weekly_task import WeeklyTask
from .challenge import MiniChallenge
from .challenges_history import ChallengeHistory
from .schedule_msg import ScheduleMessage
from .leaderbord import LeadBord

from sqlalchemy.orm import declarative_base

Base = declarative_base()
