from aiogram import Bot
from database.db import db


async def send_schedul_msg(bot: Bot, msg_id):
    print("send_schedul_msg successfully executed")
    msg_info = await db.get_schedule_message_by_id(msg_id)
    users = await db.get_users()

    if msg_info:
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=msg_info.text,
                )
            except Exception as ex:
                print(f"ERROR WHILE SEND SCHEDULED MESSAGE: {ex}")

    if msg_info.date == "every_day" or msg_info.date == "every_week":
        pass
    else:
        await db.delete_schedule_message(msg_id)
