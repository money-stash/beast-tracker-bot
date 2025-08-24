from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    FSInputFile,
)

from database.db import db

router = Router()


@router.callback_query(F.data.startswith("open_sched_msg:"))
async def print_info_schedule(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    msg_info = await db.get_schedule_message_by_id(
        msg_id=call.data.split("open_sched_msg:")[-1]
    )

    msg_text = f"📅 You opened info about scheduled message\n\n"

    msg_text += f"text: {msg_info.text}\n"
    msg_text += f"date: {msg_info.date}\n"
    msg_text += f"repeat: {msg_info.repeat}\n"
    msg_text += f"time: {msg_info.time}\n"
    msg_text += f"media_path: {msg_info.media_path}\n"

    kb = [
        [
            InlineKeyboardButton(
                text="🗑️ Delete message", callback_data=f"delete_scheduled_{msg_info.id}"
            )
        ],
        [InlineKeyboardButton(text="🔙 Back", callback_data=f"scheduled_messages")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    if msg_info.media_path == "None":
        await bot.edit_message_text(
            chat_id=user_id, message_id=call.message.message_id, text=msg_info
        )
    else:
        media_path = Path(msg_info.media_path)

        await bot.delete_message(user_id, call.message.message_id)

        media_file = FSInputFile(media_path)
        if media_path.suffix.lower() == ".mp4":
            await bot.send_video(
                chat_id=user_id,
                video=media_file,
                caption=msg_text,
                reply_markup=keyboard,
            )
        else:
            await bot.send_photo(
                chat_id=user_id,
                photo=media_file,
                caption=msg_text,
                reply_markup=keyboard,
            )
