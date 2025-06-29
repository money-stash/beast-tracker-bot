from pytz import timezone

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.user import user_commands
from callbacks.user import (
    open_profile,
    back_to_main,
    daily_ok,
    open_daily_tasks,
    add_daily_task,
    delete_daily_task,
    set_done_daily,
)
from callbacks.admin import (
    open_admin,
    open_group_settings,
    change_group,
    open_dashboard,
    cancel_admin,
    open_mem_directory,
    ban_user,
    open_settings,
    open_daily_motivation,
    open_messages_center,
    open_partner_manager,
    change_partnet_rotation,
)

from middlewares.user_info import UserInfoMiddleware
from utils.remainders import shchedule_daily_remainders

from database.db import db
from config import TOKEN, ADMIN_ID


async def scheduled_task(bot: Bot):
    await db.cleanup_daily_tasks()


async def main():
    await db.init_models()

    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.outer_middleware(UserInfoMiddleware())
    dp.callback_query.outer_middleware(UserInfoMiddleware())

    dp.include_routers(
        user_commands.router,
        open_profile.router,
        back_to_main.router,
        daily_ok.router,
        open_daily_tasks.router,
        add_daily_task.router,
        delete_daily_task.router,
        set_done_daily.router,
        open_admin.router,
        open_group_settings.router,
        change_group.router,
        open_dashboard.router,
        cancel_admin.router,
        open_mem_directory.router,
        ban_user.router,
        open_settings.router,
        open_daily_motivation.router,
        open_messages_center.router,
        open_partner_manager.router,
        change_partnet_rotation.router,
    )

    us_tz = timezone("America/New_York")

    scheduler = AsyncIOScheduler(timezone=us_tz)
    scheduler.add_job(
        scheduled_task, CronTrigger(hour=0, minute=0, timezone=us_tz), args=[bot]
    )
    scheduler.add_job(
        db.back_daily_to_history, CronTrigger(hour=23, minute=59, timezone=us_tz)
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=12, minute=0, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=17, minute=0, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=22, minute=0, timezone=us_tz),
        args=[bot],
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
