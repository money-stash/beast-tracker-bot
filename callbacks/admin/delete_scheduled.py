import os
from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    FSInputFile,
)

from keyboards.inline.admin import get_back_to_admin
from database.db import db

router = Router()


@router.callback_query(F.data.startswith("delete_scheduled_"))
async def start_del_scheduled(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    msg_id = call.data.split("delete_scheduled_")[-1]
    msg_info = await db.get_schedule_message_by_id(msg_id)

    await bot.delete_message(user_id, call.message.message_id)

    msg_text = f"Are you sure that you wanna delete this message?:\n\n"

    msg_text += f"text: {msg_info.text}\n"
    msg_text += f"date: {msg_info.date}\n"
    msg_text += f"repeat: {msg_info.repeat}\n"
    msg_text += f"time: {msg_info.time}\n"
    msg_text += f"media_path: {msg_info.media_path}\n"

    kb = [
        [
            InlineKeyboardButton(
                text="✅ Accept", callback_data=f"accept_del_schedule_{msg_id}"
            )
        ],
        [InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    if msg_info.media_path == "None":
        await bot.send_message(chat_id=user_id, text=msg_text)
    else:
        media_path = Path(msg_info.media_path)

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


@router.callback_query(F.data.startswith("accept_del_schedule_"))
async def start_del_scheduled(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    msg_id = call.data.split("accept_del_schedule_")[-1]
    msg_info = await db.get_schedule_message_by_id(msg_id)
    await db.delete_schedule_message(msg_id)

    try:
        os.remove(msg_info.media_path)
    except:
        pass

    await bot.delete_message(user_id, call.message.message_id)
    await bot.send_message(
        chat_id=user_id,
        text="✅ Message was successfully deleted!",
        reply_markup=await get_back_to_admin(),
    )
