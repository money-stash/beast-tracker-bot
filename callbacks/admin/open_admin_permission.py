from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import db
from utils.json_utils import get_group_id

router = Router()


@router.callback_query(F.data == "open_admin_permission")
async def open_list_perm_for_admin(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    users = await db.get_users()

    kb = []

    for user in users:
        kb.append(
            [
                InlineKeyboardButton(
                    text=f"{user.first_name}",
                    callback_data=f"open_perm_{user.user_id}",
                )
            ]
        )
    kb.append(
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        text="👥 Pick a user to change permissions",
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )
