import os
import csv
from tempfile import gettempdir

from random import randint, choice

from pytz import timezone
from datetime import datetime, timedelta
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.base import Base
from utils.logger import logger
from utils.time_utils import get_us_date

from models.user import User
from models.leaderbord import LeadBord
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

    async def assign_random_partners(self):
        async with self.get_session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

            if len(users) < 2:
                for user in users:
                    user.partner_id = 0
                await session.commit()
                return

            # очистка старых партнеров
            for user in users:
                user.partner_id = 0

            await session.commit()

            from random import shuffle

            user_pool = users[:]
            shuffle(user_pool)

            # если нечетное количество, один останется без партнера
            if len(user_pool) % 2 != 0:
                user_pool.pop().partner_id = 0

            pairs = []
            for i in range(0, len(user_pool), 2):
                user_a = user_pool[i]
                user_b = user_pool[i + 1]
                user_a.partner_id = user_b.user_id
                user_b.partner_id = user_a.user_id
                pairs.append((user_a.user_id, user_b.user_id))

            await session.commit()

    async def get_partners_overview(self) -> str:
        async with self.get_session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

            # Создаем словарь user_id -> username или first_name для удобства вывода
            user_map = {
                user.user_id: user.username or user.first_name or str(user.user_id)
                for user in users
            }

            lines = []
            for user in users:
                partner_id = user.partner_id
                partner_name = (
                    user_map.get(partner_id, "None")
                    if partner_id and partner_id != 0
                    else "No partner"
                )
                user_name = user_map.get(user.user_id, str(user.user_id))
                lines.append(
                    f"{user_name} (ID: {user.user_id}) — Partner: {partner_name} (ID: {partner_id})"
                )

            return "\n".join(lines)

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

    # STRAK

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

    async def set_user_streak(self, user_id: int, target_streak: int):
        async with self.get_session() as session:
            result = await session.execute(
                select(DailyHistory)
                .where(DailyHistory.user_id == user_id)
                .order_by(DailyHistory.date.asc())
            )
            history = result.scalars().all()
            history_by_date = {
                datetime.strptime(h.date, "%Y-%m-%d").date(): h for h in history
            }

            today = datetime.now(us_tz).date()
            start_date = today - timedelta(days=target_streak - 1)

            # set required dates as done
            for i in range(target_streak):
                date = start_date + timedelta(days=i)
                if date in history_by_date:
                    history_by_date[date].is_done = True
                else:
                    task_result = await session.execute(
                        select(DailyTask)
                        .where(DailyTask.user_id == user_id)
                        .order_by(DailyTask.created_date.desc())
                    )
                    task = task_result.scalar_one_or_none()
                    if task:
                        new_entry = DailyHistory(
                            user_id=user_id,
                            task_id=task.id,
                            date=date.strftime("%Y-%m-%d"),
                            is_done=True,
                        )
                        session.add(new_entry)

            # unset dates after the streak
            for h in history:
                h_date = datetime.strptime(h.date, "%Y-%m-%d").date()
                if h_date > today:
                    continue
                if h_date < start_date or h_date > today:
                    h.is_done = False

            await session.commit()

    async def get_biggest_comeback(self) -> dict:
        async with self.get_session() as session:
            users = await self.get_users()
            max_gap = 0
            max_comeback_streak = 0
            max_user = None

            for user in users:
                result = await session.execute(
                    select(DailyHistory)
                    .where(DailyHistory.user_id == user.user_id)
                    .order_by(DailyHistory.date.asc())
                )
                history = result.scalars().all()
                if not history:
                    continue

                dates_done = sorted(
                    datetime.strptime(h.date, "%Y-%m-%d").date()
                    for h in history
                    if h.is_done
                )
                if not dates_done:
                    continue

                gaps = []
                prev_date = dates_done[0]

                for i in range(1, len(dates_done)):
                    diff = (dates_done[i] - prev_date).days
                    if diff > 1:
                        gap = diff - 1
                        gaps.append((prev_date, gap, i))
                    prev_date = dates_done[i]

                if not gaps:
                    continue

                for prev_date, gap, idx in gaps:
                    current_streak = 1
                    for j in range(idx + 1, len(dates_done)):
                        if (dates_done[j] - dates_done[j - 1]).days == 1:
                            current_streak += 1
                        else:
                            break
                    if gap > max_gap or (
                        gap == max_gap and current_streak > max_comeback_streak
                    ):
                        max_gap = gap
                        max_comeback_streak = current_streak
                        max_user = user

            if max_user is None:
                return {}

            return {
                "user_id": max_user.user_id,
                "max_gap": max_gap,
                "comeback_streak": max_comeback_streak,
            }

    async def get_most_consistent_this_month(self) -> dict:
        async with self.get_session() as session:
            users = await self.get_users()
            if not users:
                return {}

            now = datetime.now(us_tz)
            first_day = now.replace(day=1).date()
            last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(
                days=1
            )
            max_done = 0
            most_consistent_user = None

            for user in users:
                result = await session.execute(
                    select(DailyHistory).where(
                        DailyHistory.user_id == user.user_id,
                        DailyHistory.is_done == True,
                        DailyHistory.date >= first_day.strftime("%Y-%m-%d"),
                        DailyHistory.date <= last_day.strftime("%Y-%m-%d"),
                    )
                )
                done_days = result.scalars().all()
                count_done = len(done_days)

                if count_done > max_done:
                    max_done = count_done
                    most_consistent_user = user

            if most_consistent_user is None:
                return {}

            return {
                "user_id": most_consistent_user.user_id,
                "first_name": most_consistent_user.first_name,
                "username": most_consistent_user.username,
                "done_days": max_done,
            }

    ##########                             ##########
    ##########          TABLE UTILS        ##########
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

    async def update_leaderboard(self):
        async with self.get_session() as session:
            users = await self.get_users()
            streaks = []

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

                streaks.append((user.user_id, streak))

            top_streaks = sorted(streaks, key=lambda x: x[1], reverse=True)[:5]

            await session.execute(delete(LeadBord))  # удаляем все записи перед записью
            for user_id, streak in top_streaks:
                entry = LeadBord(user_id=user_id, streak=streak)
                session.add(entry)

            await session.commit()
            logger.info("leaderboard updated")

    async def get_leaderboard(self):
        async with self.get_session() as session:
            result = await session.execute(
                select(LeadBord).order_by(LeadBord.streak.desc())
            )
            entries = result.scalars().all()
            return entries

    async def export_all_users_report(self) -> str:
        # Собираем всех пользователей
        users = await self.get_users()

        # Создаем файл во временной папке
        filename = "all_users_full_report.csv"
        filepath = os.path.join(gettempdir(), filename)

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for user in users:
                # Заголовок для каждого пользователя
                writer.writerow([f"===== USER: {user.username} ({user.user_id}) ====="])
                writer.writerow([])

                # 1) Daily Check-ins (current tasks)
                writer.writerow(["== CURRENT DAILY TASKS =="])
                writer.writerow(["Date", "Task Text", "Done"])
                current_tasks = await self.get_daily_tasks(user.user_id)
                for task in current_tasks:
                    writer.writerow(
                        [
                            task.created_date,
                            task.daily_task,
                            "Yes" if task.is_done else "No",
                        ]
                    )
                writer.writerow([])

                # 2) Daily History
                writer.writerow(["== DAILY HISTORY =="])
                writer.writerow(["Date", "Task ID", "Done"])
                async with self.get_session() as session:
                    history_result = await session.execute(
                        select(DailyHistory)
                        .where(DailyHistory.user_id == user.user_id)
                        .order_by(DailyHistory.date.asc())
                    )
                    daily_history = history_result.scalars().all()
                    for entry in daily_history:
                        writer.writerow(
                            [
                                entry.date,
                                entry.task_id,
                                "Yes" if entry.is_done else "No",
                            ]
                        )
                writer.writerow([])

                # 3) Missed Days
                missed = await self.get_missed_daily_days(user.user_id)
                writer.writerow(["== MISSED DAYS =="])
                writer.writerow(["Total Missed Days", missed])
                writer.writerow([])

                # 4) Current Streak
                current_streak = await self.get_current_daily_streak(user.user_id)
                writer.writerow(["== STREAK INFO =="])
                writer.writerow(["Current Streak", current_streak])
                writer.writerow([])

                # 5) Partner Data
                writer.writerow(["== USER DATA =="])
                writer.writerow(["Username", user.username or "N/A"])
                writer.writerow(["First Name", user.first_name or "N/A"])
                writer.writerow(["Partner ID", user.partner_id or "No partner"])
                writer.writerow(["Registration Date", user.reg_date or "N/A"])
                writer.writerow(
                    ["Is Banned", "Yes" if getattr(user, "is_baned", False) else "No"]
                )
                writer.writerow([])

                # 6) Challenge Logs
                writer.writerow(["== CHALLENGE LOGS =="])
                writer.writerow(["Date", "Challenge ID", "Executed"])
                async with self.get_session() as session:
                    challenge_result = await session.execute(
                        select(ChallengeHistory)
                        .where(ChallengeHistory.user_id == user.user_id)
                        .order_by(ChallengeHistory.date.asc())
                    )
                    challenge_history = challenge_result.scalars().all()
                    for entry in challenge_history:
                        writer.writerow(
                            [
                                entry.date,
                                entry.challenge_id,
                                "Yes" if entry.is_executed else "No",
                            ]
                        )
                writer.writerow([])

                # 7) Overall Participation
                writer.writerow(["== OVERALL PARTICIPATION =="])
                total_current_checkins = len([t for t in current_tasks if t.is_done])
                total_history_checkins = len([h for h in daily_history if h.is_done])
                total_challenges = len(challenge_history)
                writer.writerow(["Current Tasks Done", total_current_checkins])
                writer.writerow(["Historical Tasks Done", total_history_checkins])
                writer.writerow(["Total Challenges Logged", total_challenges])
                writer.writerow([])
                writer.writerow([])
                writer.writerow([])  # Дополнительная пустая строка между пользователями

        return filepath

    async def export_checkin_report(self) -> str:
        users = await self.get_users()
        filename = "all_users_checkin_report.csv"
        filepath = os.path.join(gettempdir(), filename)

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["User ID", "Username", "First Name", "Date", "Task Text", "Done"]
            )

            async with self.get_session() as session:
                for user in users:
                    history_result = await session.execute(
                        select(DailyHistory)
                        .where(DailyHistory.user_id == user.user_id)
                        .order_by(DailyHistory.date.asc())
                    )
                    history = history_result.scalars().all()

                    for entry in history:
                        task_result = await session.execute(
                            select(DailyTask).where(DailyTask.id == entry.task_id)
                        )
                        task = task_result.scalar_one_or_none()
                        task_text = task.daily_task if task else "Unknown Task"
                        writer.writerow(
                            [
                                user.user_id,
                                user.username or "",
                                user.first_name or "",
                                entry.date,
                                task_text,
                                "Yes" if entry.is_done else "No",
                            ]
                        )

        return filepath

    async def get_dme_stats(self, user_id: int) -> str:
        async with self.get_session() as session:
            today = datetime.now(us_tz).date()
            day_7 = today - timedelta(days=6)
            day_30 = today - timedelta(days=29)
            day_90 = today - timedelta(days=89)

            result = await session.execute(
                select(DailyHistory).where(DailyHistory.user_id == user_id)
            )
            history = result.scalars().all()

            if not history:
                return "No data available."

            # Get user's registration/start date
            earliest_record_date = min(
                datetime.strptime(h.date, "%Y-%m-%d").date() for h in history if h.date
            )

            def calc_rate(start_date=None, period_name=None):
                # For "Today", only check today's completion
                if period_name == "Today":
                    today_record = next(
                        (h for h in history if h.date == today.strftime("%Y-%m-%d")),
                        None,
                    )
                    if today_record:
                        return "100%" if today_record.is_done else "0%"
                    else:
                        return "0%"  # No record for today means not done

                # For period calculations, check if user has been active long enough
                if start_date and earliest_record_date > start_date:
                    return "N/A"

                day_map = {}
                for h in history:
                    if not h.date:
                        continue
                    h_date = datetime.strptime(h.date, "%Y-%m-%d").date()
                    if start_date and h_date < start_date:
                        continue
                    if h_date not in day_map:
                        day_map[h_date] = h.is_done
                    else:
                        day_map[h_date] = day_map[h_date] or h.is_done

                if not day_map:
                    return "N/A"

                done_days = sum(1 for v in day_map.values() if v)
                total_days = len(day_map)
                return f"{round(done_days / total_days * 100)}%"

            def get_longest_streak():
                dates = sorted(
                    datetime.strptime(h.date, "%Y-%m-%d").date()
                    for h in history
                    if h.is_done
                )
                if not dates:
                    return "0 Days"
                streak = max_streak = 1
                best_day = dates[0]
                for i in range(1, len(dates)):
                    if (dates[i] - dates[i - 1]).days == 1:
                        streak += 1
                        if streak > max_streak:
                            max_streak = streak
                            best_day = dates[i]
                    else:
                        streak = 1
                return f"{max_streak} Days on {best_day.strftime('%B %d, %Y')}"

            def get_badges():
                days = sorted(
                    set(
                        datetime.strptime(h.date, "%Y-%m-%d").date()
                        for h in history
                        if h.is_done
                    )
                )
                if not days:
                    return []
                badges = []
                streak = 1
                for i in range(1, len(days)):
                    if (days[i] - days[i - 1]).days == 1:
                        streak += 1
                        if streak in [7, 30, 60, 90, 120] and streak not in badges:
                            badges.append(streak)
                    else:
                        streak = 1
                return [f"{d}-day Streak" for d in badges]

            all_users = await self.get_users()
            ranks = []
            for user in all_users:
                if user.user_id == user_id:
                    continue
                other_result = await session.execute(
                    select(DailyHistory)
                    .where(DailyHistory.user_id == user.user_id)
                    .order_by(DailyHistory.date.asc())
                )
                other_hist = other_result.scalars().all()
                streak = 0
                last_date = None
                for entry in reversed(other_hist):
                    current = datetime.strptime(entry.date, "%Y-%m-%d").date()
                    if last_date is None:
                        if (today - current).days > 1:
                            break
                        streak = 1
                    else:
                        diff = (last_date - current).days
                        if diff == 1:
                            streak += 1
                        elif diff == 0:
                            continue
                        else:
                            break
                    last_date = current
                ranks.append(streak)

            current_streak = await self.get_current_daily_streak(user_id)
            unstoppable_rank = sum(s < current_streak for s in ranks) + 1
            total_users = len(all_users)

            stats = f"""DME Completion Rate:
        Today: {calc_rate(None, "Today")}
        Last 7 Days: {calc_rate(day_7, "7 Days")}
        Last 30 Days: {calc_rate(day_30, "30 Days")}
        Last 90 Days: {calc_rate(day_90, "90 Days")}
        Since starting: {calc_rate(None)}
        Longest Streak: {get_longest_streak()}
        UNSTOPPABLE Rank: {unstoppable_rank} of {total_users}
        Badges Earned: ({len(get_badges())}) - {', '.join(get_badges()) if get_badges() else 'None'}"""

            return stats


db = Database()
