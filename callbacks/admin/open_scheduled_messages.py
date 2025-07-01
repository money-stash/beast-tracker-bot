from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from database.db import db
from keyboards.inline.admin import get_challenges_menu

router = Router()


@router.callback_query(F.data == "scheduled_messages")
async def print_scheduled_messages(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    msgs = await db.get_all_schedule_messages()
    kb = []

    for msg in msgs:
        if msg.date not in ["every_day", "every_week"]:
            try:
                date_obj = datetime.strptime(msg.date, "%Y-%m-%d")
                if date_obj < datetime.now():
                    continue
            except ValueError:
                continue

        kb.append(
            [
                InlineKeyboardButton(
                    text=f"🕰️ {msg.time} | {msg.text[:20]}...",
                    callback_data=f"open_sched_msg:{msg.id}",
                )
            ]
        )

    kb.append([InlineKeyboardButton(text="🔙 Back", callback_data="open_motivation")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.delete_message(user_id, call.message.message_id)

    await bot.send_message(
        text="📋 All scheduled messages:",
        reply_markup=keyboard,
        chat_id=user_id,
    )
