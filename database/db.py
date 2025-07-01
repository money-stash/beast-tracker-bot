import os
import csv
from tempfile import gettempdir

from random import randint

from pytz import timezone
from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.base import Base
from utils.logger import logger
from utils.time_utils import get_us_date

from models.user import User
from models.daily_task import DailyTask
from models.weekly_task import WeeklyTask
from models.challenge import MiniChallenge
from models.daily_history import DailyHistory
from models.challenges_history import ChallengeHistory
from models.schedule_msg import ScheduleMessage

from config import DB_PATH, us_tz


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()

        return cls._instance

    def _init(self):
        self.database_url = f"sqlite+aiosqlite:///{DB_PATH}"
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def init_models(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            logger.info("Database initialized")

        except Exception as e:
            logger.error(f"Error initializing DB: {e}")

    def get_session(self) -> AsyncSession:
        return self.async_session()

    ##########                          ##########
    ##########      User methods        ##########
    ##########                          ##########

    async def create_user(self, user_id: int, first_name: str, username: str):
        async with self.get_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            reg_date = get_us_date()

            if user is None:
                user = User(
                    user_id=user_id,
                    first_name=first_name,
                    username=username,
                    reg_date=reg_date,
                )
                session.add(user)
                await session.commit()
                logger.info(f"User {user_id} created")
            else:
                logger.info(f"User {user_id} already exists")

    async def get_users(self) -> list[User]:
        async with self.get_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def get_user(self, user_id: int) -> User | None:
        async with self.get_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.scalar_one_or_none()

    async def find_user(self, identifier: str):
        if identifier.isdigit():
            user = await self.get_user(int(identifier))
            return user if user else False

        identifier = identifier.strip()

        if identifier.startswith("https://t.me/"):
            username = identifier.split("/")[-1]
        elif identifier.startswith("@"):
            username = identifier[1:]
        else:
            username = identifier.lstrip("@")

        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            user = result.scalar_one_or_none()
            return user if user else False

    async def update_user_balance(self, user_id: int, balance: float):
        async with self.get_session() as session:
            await session.execute(
                update(User).where(User.user_id == user_id).values(balance=balance)
            )
            await session.commit()

    async def updated_username(self, user_id: int, username: str):
        async with self.get_session() as session:
            await session.execute(
                update(User).where(User.user_id == user_id).values(username=username)
            )
            await session.commit()

            logger.info(f"User {user_id}(username) updated")

    async def delete_user(self, user_id: int):
        async with self.get_session() as session:
            await session.execute(delete(User).where(User.user_id == user_id))
            await session.commit()

    async def ban_user(self, user_id: int, banned: bool):
        async with self.get_session() as session:
            await session.execute(
                update(User).where(User.user_id == user_id).values(is_baned=banned)
            )
            await session.commit()
            logger.info(f"User {user_id} banned={banned}")

    ##########                          ##########
    ##########    MiniChallenge CRUD    ##########
    ##########                          ##########

    async def add_challenge(self, name: str, duration: int, rules: str, action: str):
        async with self.get_session() as session:
            rand_id = randint(1, 1000000)
            challenge = MiniChallenge(
                id=rand_id, name=name, duration=duration, rules=rules, action=action
            )
            session.add(challenge)
            await session.commit()
            logger.info(f"Challenge '{name}' added")

    async def delete_challenge(self, challenge_id: int):
        async with self.get_session() as session:
            await session.execute(
                delete(MiniChallenge).where(MiniChallenge.id == challenge_id)
            )
            await session.commit()
            logger.info(f"Challenge with id {challenge_id} deleted")

    async def get_all_challenges(self) -> list[MiniChallenge]:
        async with self.get_session() as session:
            result = await session.execute(select(MiniChallenge))
            return result.scalars().all()

    async def get_challenge_by_id(self, challenge_id: int) -> MiniChallenge | None:
        async with self.get_session() as session:
            result = await session.execute(
                select(MiniChallenge).where(MiniChallenge.id == challenge_id)
            )
            return result.scalar_one_or_none()

    ##########                          ##########
    ##########      Daily tasks         ##########
    ##########                          ##########

    # set is_done to False for all tasks
    async def cleanup_daily_tasks(self):
        async with self.get_session() as session:
            tasks_result = await session.execute(select(DailyTask))
            tasks = tasks_result.scalars().all()

            now_date = datetime.now(timezone(us_tz)).strftime("%Y-%m-%d")

            for task in tasks:
                history = DailyHistory(
                    user_id=task.user_id,
                    task_id=task.id,
                    date=now_date,
                    is_done=task.is_done,
                )
                session.add(history)

            await session.execute(update(DailyTask).values(is_done=False))
            await session.commit()

            logger.info("Daily tasks cleaned up and history saved")

    async def create_daily_task(self, user_id: int, task_text: str, date: str):
        async with self.get_session() as session:
            task = DailyTask(user_id=user_id, daily_task=task_text, created_date=date)
            session.add(task)
            await session.commit()

            logger.info(f"Daily task created for user {user_id}")

    async def get_daily_tasks(self, user_id: int) -> list[DailyTask]:
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyTask).where(DailyTask.user_id == user_id)
            )
            return result.scalars().all()

    async def get_daily_task(self, task_id: int) -> DailyTask | None:
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyTask).where(DailyTask.id == task_id)
            )
            return result.scalar_one_or_none()

    async def mark_task_done(self, task_id: int, done_status: bool):
        async with self.get_session() as session:
            await session.execute(
                update(DailyTask)
                .where(DailyTask.id == task_id)
                .values(is_done=done_status)
            )
            await session.commit()

            logger.info(f"Task {task_id} marked as done")

    async def delete_task(self, task_id: int):
        async with self.get_session() as session:
            await session.execute(delete(DailyTask).where(DailyTask.id == task_id))
            await session.commit()

            logger.info(f"Task {task_id} deleted")

    async def back_daily_to_history(self):
        print("back_daily_to_history successffully executed")
        async with self.get_session() as session:
            users = await self.get_users()
            for user in users:
                all_tasks = await self.get_daily_tasks(user.user_id)
                for task in all_tasks:
                    if task.is_done:
                        history = DailyHistory(
                            user_id=user.user_id,
                            task_id=task.id,
                            date=datetime.now(us_tz).strftime("%Y-%m-%d"),
                            is_done=True,
                        )
                        session.add(history)
                        await session.commit()

                        await self.mark_task_done(task.id, False)
            logger.info("Daily tasks moved to history")

    async def daily_user_remainder(self, user_id: int):
        async with self.get_session() as session:
            user_tasks = await self.get_daily_tasks(user_id)
            unfinished_tasks = []

            for task in user_tasks:
                if not task.is_done:
                    unfinished_tasks.append(task)

            return unfinished_tasks

    async def count_users_completed_all_tasks_today(self) -> int:
        async with self.get_session() as session:
            users = await self.get_users()
            completed_users = 0

            for user in users:
                result = await session.execute(
                    select(DailyTask).where(DailyTask.user_id == user.user_id)
                )
                tasks = result.scalars().all()
                if tasks and all(task.is_done for task in tasks):
                    completed_users += 1

            return completed_users

    ##########                                  ##########
    ##########    ChallengeHistory methods       ##########
    ##########                                  ##########

    async def upsert_challenge_history(
        self, challenge_id: int, user_id: int, executed: bool
    ):
        async with self.get_session() as session:
            current_date = datetime.now(us_tz).strftime("%Y-%m-%d")
            result = await session.execute(
                select(ChallengeHistory).where(
                    ChallengeHistory.challenge_id == challenge_id,
                    ChallengeHistory.user_id == user_id,
                    ChallengeHistory.date == current_date,
                )
            )
            entry = result.scalar_one_or_none()

            if entry:
                entry.is_executed = executed
            else:
                entry = ChallengeHistory(
                    challenge_id=challenge_id,
                    user_id=user_id,
                    date=current_date,
                    is_executed=executed,
                )
                session.add(entry)

            await session.commit()
            logger.info(
                f"Challenge history updated: user={user_id}, challenge={challenge_id}, executed={executed}"
            )

    async def is_challenge_executed_today(
        self, challenge_id: int, user_id: int
    ) -> bool:
        async with self.get_session() as session:
            current_date = datetime.now(us_tz).strftime("%Y-%m-%d")
            result = await session.execute(
                select(ChallengeHistory).where(
                    ChallengeHistory.challenge_id == challenge_id,
                    ChallengeHistory.user_id == user_id,
                    ChallengeHistory.date == current_date,
                )
            )
            entry = result.scalar_one_or_none()
            return entry.is_executed if entry else False

    async def check_all_challenges_today(self):
        print("check_all_challenges_today successffully executed")
        async with self.get_session() as session:
            users = await self.get_users()
            challenges = await self.get_all_challenges()
            logger.info(
                f"Checking challenges for {len(users)} users and {len(challenges)} challenges"
            )

            for user in users:
                for challenge in challenges:
                    result = await session.execute(
                        select(ChallengeHistory).where(
                            ChallengeHistory.challenge_id == challenge.id,
                            ChallengeHistory.user_id == user.user_id,
                            ChallengeHistory.date
                            == datetime.now(timezone(us_tz)).strftime("%Y-%m-%d"),
                        )
                    )
                    exists = result.scalar_one_or_none()
                    if not exists:
                        await self.upsert_challenge_history(
                            challenge.id, user.user_id, False
                        )
                        logger.info(
                            f"Marked as not executed: user={user.user_id}, challenge={challenge.id}"
                        )

    ##########                             ##########
    ##########    ScheduleMessage CRUD     ##########
    ##########                             ##########

    async def add_schedule_message(
        self, text: str, media_path: str, date: str, time: str, repeat: str
    ) -> ScheduleMessage:
        async with self.get_session() as session:
            msg = ScheduleMessage(
                id=randint(1, 1000000),
                text=text,
                media_path=media_path,
                date=date,
                time=time,
                repeat=repeat,
            )
            session.add(msg)

            await session.commit()
            await session.refresh(msg)

            logger.info(f"Scheduled message added: id={msg.id}")

            return msg

    async def delete_schedule_message(self, msg_id: int):
        async with self.get_session() as session:
            await session.execute(
                delete(ScheduleMessage).where(ScheduleMessage.id == msg_id)
            )
            await session.commit()
            logger.info(f"Scheduled message deleted: id={msg_id}")

    async def get_all_schedule_messages(self) -> list[ScheduleMessage]:
        async with self.get_session() as session:
            result = await session.execute(select(ScheduleMessage))
            return result.scalars().all()

    async def get_schedule_message_by_id(self, msg_id: int) -> ScheduleMessage | None:
        async with self.get_session() as session:
            result = await session.execute(
                select(ScheduleMessage).where(ScheduleMessage.id == msg_id)
            )
            return result.scalar_one_or_none()

    async def get_user_with_longest_daily_streak(
        self, user_id: int | None = None
    ) -> dict:
        async with self.get_session() as session:
            if user_id is not None:
                users = [await self.get_user(user_id)]
                if users[0] is None:
                    return {}
            else:
                users = await self.get_users()

            max_streak_user = None
            max_streak = 0

            for user in users:
                result = await session.execute(
                    select(DailyHistory)
                    .where(
                        DailyHistory.user_id == user.user_id,
                        DailyHistory.is_done == True,
                    )
                    .order_by(DailyHistory.date.asc())
                )
                history = result.scalars().all()

                streak = 0
                longest_streak = 0
                last_date = None

                for entry in history:
                    current_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
                    if last_date is None:
                        streak = 1
                    else:
                        diff = (current_date - last_date).days
                        if diff == 1:
                            streak += 1
                        elif diff == 0:
                            continue
                        else:
                            streak = 1
                    last_date = current_date
                    longest_streak = max(longest_streak, streak)

                if longest_streak > max_streak:
                    max_streak = longest_streak
                    max_streak_user = user

            if max_streak_user:
                return {
                    "user_id": max_streak_user.user_id,
                    "first_name": max_streak_user.first_name,
                    "username": max_streak_user.username,
                    "max_streak": max_streak,
                }
            return {}

    async def get_current_daily_streak(self, user_id: int) -> int:
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyHistory)
                .where(DailyHistory.user_id == user_id, DailyHistory.is_done == True)
                .order_by(DailyHistory.date.asc())
            )
            history = result.scalars().all()

            if not history:
                return 0

            streak = 0
            last_date = None

            for entry in reversed(history):
                current_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
                if last_date is None:
                    if (datetime.now(us_tz).date() - current_date).days > 1:
                        break
                    streak = 1
                else:
                    diff = (last_date - current_date).days
                    if diff == 1:
                        streak += 1
                    elif diff == 0:
                        continue
                    else:
                        break
                last_date = current_date

            return streak

    async def get_missed_daily_days(self, user_id: int) -> int:
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyHistory)
                .where(DailyHistory.user_id == user_id)
                .order_by(DailyHistory.date.asc())
            )
            history = result.scalars().all()

            if not history:
                return 0

            dates = sorted(
                {datetime.strptime(entry.date, "%Y-%m-%d").date() for entry in history}
            )
            if not dates:
                return 0

            full_range = (dates[-1] - dates[0]).days + 1
            unique_dates = {
                date
                for date in dates
                if any(
                    h.date == date.strftime("%Y-%m-%d") and h.is_done for h in history
                )
            }

            return full_range - len(unique_dates)

    ##########                             ##########
    ##########          TALBE UTILS        ##########
    ##########                             ##########

    async def export_user_daily_history(self, user_id: int) -> str:
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyHistory)
                .where(DailyHistory.user_id == user_id)
                .order_by(DailyHistory.date.asc())
            )
            history = result.scalars().all()

            if not history:
                return ""

            filename = f"user_{user_id}_daily_history.csv"
            filepath = os.path.join(gettempdir(), filename)

            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Task Text", "Is Done"])

                for entry in history:
                    task_result = await session.execute(
                        select(DailyTask).where(DailyTask.id == entry.task_id)
                    )
                    task = task_result.scalar_one_or_none()
                    task_text = task.daily_task if task else "Unknown Task"
                    writer.writerow(
                        [entry.date, task_text, "Yes" if entry.is_done else "No"]
                    )

            return filepath


db = Database()
