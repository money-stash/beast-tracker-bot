from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

from database.db import db
from utils.logger import logger

router = Router()


@router.callback_query(F.data == "done_daily_task")
async def open_remove_daily_task(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id

    daily_user = await db.get_daily_tasks(user_id)

    kb = []

    for task in daily_user:
        if task.is_done:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=f"✅ {task.daily_task}",
                        callback_data=f"set_done_daily_{task.id}",
                    )
                ]
            )
        else:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {task.daily_task}",
                        callback_data=f"set_done_daily_{task.id}",
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

    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text="❗️ Select the tasks you want to mark as completed",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("set_done_daily_"))
async def is_remove_daily_task(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    task_id = int(call.data.split("_")[3])
    data = await state.get_data()
    selected_tasks = data.get("selected_tasks", [])

    if task_id in selected_tasks:
        selected_tasks.remove(task_id)
        await db.mark_task_done(task_id, False)
    else:
        selected_tasks.append(task_id)
        await db.mark_task_done(task_id, True)

    await state.update_data(selected_tasks=selected_tasks)

    daily_user = await db.get_daily_tasks(user_id)

    kb_btns = []

    for task in daily_user:
        if task.is_done:
            kb_btns.append(
                [
                    InlineKeyboardButton(
                        text=f"✅ {task.daily_task}",
                        callback_data=f"set_done_daily_{task.id}",
                    )
                ]
            )
        else:
            kb_btns.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {task.daily_task}",
                        callback_data=f"set_done_daily_{task.id}",
                    )
                ]
            )

    kb_btns.append(
        [
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data="back_to_daily",
            )
        ]
    )

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=kb_btns)

    try:
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=inline_keyboard,
        )
    except Exception as e:  # type: ignore
        logger.error(f"Error editing message: {e}")
