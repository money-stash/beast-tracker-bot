from database.db import db
from middlewares.user import get_daily_ok


async def shchedule_daily_remainders(bot):
    all_users = await db.get_users()
    print("shchedule_daily_remainders successffully executed")

    for user in all_users:
        user_unfinished_tasks = await db.daily_user_remainder(user.user_id)

        if len(user_unfinished_tasks) == 0:
            continue

        answ_text = "📋 You have uncompleted tasks for the day:\n\n"

        for task in user_unfinished_tasks:
            answ_text += f"• {task.daily_task}\n"

        try:
            await bot.send_message(
                chat_id=user.user_id,
                text=answ_text,
                reply_markup=await get_daily_ok(),
            )
        except Exception as e:
            print(f"Error while sending daily remainder to user {user.user_id}: {e}")
