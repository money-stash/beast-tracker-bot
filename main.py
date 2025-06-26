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
from callbacks.admin import open_admin, open_group_settings, change_group

from middlewares.user_info import UserInfoMiddleware

from database.db import db
from config import TOKEN


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
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
