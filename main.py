import asyncio
from aiogram import Bot, Dispatcher

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

from middlewares.user_info import UserInfoMiddleware

from database.db import db
from config import TOKEN


async def main():
    await db.init_models()

    bot = Bot(TOKEN)
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
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
