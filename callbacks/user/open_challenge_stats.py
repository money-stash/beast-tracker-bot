from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import db
from keyboards.inline.user import get_back_to_main_menu

router = Router()


@router.callback_query(F.data.startswith("challenge_stats_"))
async def show_challenge_stats(call: CallbackQuery, bot: Bot, user_id: int):
    challenge_id = call.data.split("challenge_stats_")[-1]
    stats = await db.get_mini_challenge_stats(user_id, challenge_id)

    kb = [
        [
            InlineKeyboardButton(
                text="🔙 Back", callback_data=f"open_user_challenge_{challenge_id}"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=stats,
        reply_markup=keyboard,
    )
