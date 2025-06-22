from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database.db import db

router = Router()


@router.callback_query(F.data == "remove_daily_task")
async def open_remove_daily_task(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    daily_user = await db.get_daily_tasks(user_id)
    kb = []

    for task in daily_user:
        kb.append(
            [
                InlineKeyboardButton(
                    text=task.daily_task,
                    callback_data=f"del_daily_{task.id}",
                )
            ]
        )
    kb.append(
        [
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data="back_to_daily",
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
    )

    if len(daily_user) == 0:
        answ_text = "❗️ You have no tasks to remove"
    else:
        answ_text = "❗️ Select the task you want to delete"

    await bot.send_message(
        chat_id=call.from_user.id,
        text=answ_text,
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("del_daily_"))
async def is_remove_daily_task(call: CallbackQuery, bot: Bot):
    task_id = int(call.data.split("_")[2])
    task_info = await db.get_daily_task(task_id)

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=f"Do you really want to delete the task:\n\n"
        f"<b>{task_info.daily_task}</b>\n\n"
        f"❗️ <b>Attention!</b> Once a task is deleted, you cannot restore it.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Yes",
                        callback_data=f"confirm_del_daily_{task_id}",
                    ),
                    InlineKeyboardButton(
                        text="❌ No",
                        callback_data="back_to_daily",
                    ),
                ]
            ]
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("confirm_del_daily_"))
async def confirm_remove_daily_task(call: CallbackQuery, bot: Bot):
    task_id = int(call.data.split("_")[3])
    task_info = await db.get_daily_task(task_id)

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=f"✅ Task <b>{task_info.daily_task}</b> successfully deleted",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Back",
                        callback_data="back_to_daily",
                    )
                ]
            ]
        ),
        parse_mode="HTML",
    )

    await db.delete_task(task_id)
