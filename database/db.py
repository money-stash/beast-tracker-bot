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
from models.daily_history import DailyHistory
from models.weekly_task import WeeklyTask

from config import DB_PATH


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

    ##########                          ##########
    ##########      Daily tasks         ##########
    ##########                          ##########

    # set is_done to False for all tasks
    async def cleanup_daily_tasks(self):
        async with self.get_session() as session:
            tasks_result = await session.execute(select(DailyTask))
            tasks = tasks_result.scalars().all()

            now_date = datetime.now(timezone("Europe/Kyiv")).strftime("%Y-%m-%d")

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
        async with self.get_session() as session:
            users = await self.get_users()
            for user in users:
                all_tasks = await self.get_daily_tasks(user.user_id)
                for task in all_tasks:
                    if task.is_done:
                        history = DailyHistory(
                            user_id=user.user_id,
                            task_id=task.id,
                            date=datetime.now(timezone("Europe/Kyiv")).strftime(
                                "%Y-%m-%d"
                            ),
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


db = Database()
