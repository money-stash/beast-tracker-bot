from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from middlewares.user import get_daily_ok


async def shchedule_daily_remainders(bot):
    all_users = await db.get_users()
    print("shchedule_daily_remainders successffully executed")

    for user in all_users:
        user_unfinished_tasks = await db.daily_user_remainder(user.user_id)
        user_info = await db.get_user(user.user_id)

        if len(user_unfinished_tasks) == 0:
            continue

        answ_text = f"📋 Hi <b>{user_info.first_name}</b>!\nChecking in: Have you completed your DME for today?\n\n"

        for task in user_unfinished_tasks:
            answ_text += f"• {task.daily_task}\n"

        kb = [
            [
                InlineKeyboardButton(
                    text="💪 Yes, Mark Completed!", callback_data="done_daily_task"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="😱 Not yet. I will get it done soon.",
                    callback_data="ok_daily",
                ),
            ],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

        try:
            await bot.send_message(
                chat_id=user.user_id,
                text=answ_text,
                reply_markup=keyboard,
            )
        except Exception as e:
            print(f"Error while sending daily remainder to user {user.user_id}: {e}")
