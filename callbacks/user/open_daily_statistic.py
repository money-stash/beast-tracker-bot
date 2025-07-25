from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from middlewares.user import get_back_to_main_menu

router = Router()


@router.callback_query(F.data == "daily_statistic")
async def open_open_daily(call: CallbackQuery, bot: Bot, user_id: int):
    is_user = await db.find_user(str(user_id))

    user_streak = await db.get_current_daily_streak(is_user.user_id)
    max_streak = await db.get_user_with_longest_daily_streak(is_user.user_id)
    missed_days = await db.get_missed_daily_days(is_user.user_id)

    info = "<b>👤 USER INFO</b>\n\n"
    info += f"User_id: <code>{is_user.user_id}</code>\n"
    info += f"Username: <code>{is_user.username}</code>\n"
    info += f"First name: <code>{is_user.first_name}</code>\n"
    info += f"Reg date: <code>{is_user.reg_date}</code>\n"
    info += f"Current DME streak: <code>{user_streak}</code>\n"
    info += f"All-time streak high: <code>{max_streak['max_streak']}</code>\n"
    info += f"Total missed days: <code>{missed_days}</code>\n"

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=info,
        reply_markup=await get_back_to_main_menu(),
    )
