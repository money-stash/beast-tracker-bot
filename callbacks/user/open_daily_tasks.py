from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from middlewares.user import get_daily_menu

router = Router()


@router.callback_query(F.data == "daily_tasks")
async def open_daily_tasks(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    daily_user = await db.get_daily_tasks(user_id)
    answ_text = "📋 You have moved to the daily tasks menu\n\n"

    if len(daily_user) == 0:
        answ_text += "❗️ You don't have daily tasks"
    else:
        for task in daily_user:
            if task.is_done:
                answ_text += f"✅ {task.daily_task}\n"
            else:
                answ_text += f"⁉️ {task.daily_task}\n"

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=answ_text,
        reply_markup=await get_daily_menu(),
    )
