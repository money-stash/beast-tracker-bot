from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from keyboards.inline.admin import get_admin_menu

router = Router()


@router.callback_query(F.data == "open_admin")
async def open_admion_menu(call: CallbackQuery, bot: Bot, user_id: int):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="👩‍💼 You opened admin panel",
        reply_markup=await get_admin_menu(),
    )
