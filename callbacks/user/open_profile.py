from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from middlewares.user import get_back_to_main_menu

router = Router()


@router.callback_query(F.data == "profile")
async def open_profile(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    user_info = await db.get_user(user_id)

    answ_text = (
        f"👤 Profile\n\n"
        f"Name: {user_info.first_name}\n"
        f"Username: {user_info.username}\n"
    )

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=answ_text,
        reply_markup=await get_back_to_main_menu(),
    )
