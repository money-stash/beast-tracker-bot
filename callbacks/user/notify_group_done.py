from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

import os
import json
from datetime import date

from database.db import db
from utils.logger import logger
from utils.json_utils import get_group_id

router = Router()

NOTIFY_LOG_PATH = "database/notify_log.json"


def _load_notify_log():
    if not os.path.exists(NOTIFY_LOG_PATH):
        return {}
    try:
        with open(NOTIFY_LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except Exception:
        return {}


def _save_notify_log(data: dict) -> None:
    os.makedirs(os.path.dirname(NOTIFY_LOG_PATH), exist_ok=True)
    with open(NOTIFY_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _has_notified_today(user_id: int) -> bool:
    data = _load_notify_log()
    today = date.today().isoformat()
    last = data.get(str(user_id))
    return last == today


def _mark_notified_today(user_id: int) -> None:
    data = _load_notify_log()
    data[str(user_id)] = date.today().isoformat()
    _save_notify_log(data)


@router.callback_query(F.data == "notify_group_dme_done")
async def notify_group_dme_done(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    user_id = call.from_user.id
    # if _has_notified_today(user_id):
    #     try:
    #         await call.answer(
    #             "You have already notified the group today.", show_alert=True
    #         )
    #         await bot.edit_message_text(
    #             chat_id=user_id,
    #             message_id=call.message.message_id,
    #             text="You have already sent today's DME notification.",
    #         )
    #     except Exception as e:
    #         logger.error(f"Failed to inform about duplicate notify: {e}")
    #     return
    crnt_strak = await db.get_current_daily_streak(user_id)
    print(f"Current Streak: {crnt_strak}")

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
                        text=f"{task.daily_task}",
                        callback_data=f"set_done_daily_{task.id}",
                    )
                ]
            )

    all_ready = False
    if all(task.is_done for task in daily_user):
        all_ready = True

    kb.append(
        [
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data="back_to_daily",
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    # Check if user has already notified today
    if _has_notified_today(user_id):
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text="You have already sent today's DME notification.",
            reply_markup=keyboard,
        )
        return

    user_info = await db.get_user(user_id)
    users_uncompleted = await db.count_users_not_completed_all_tasks_today()

    group_id = get_group_id()

    try:
        msg_text = ""
        if all_ready:
            msg_text = f"🥳 Excellent work, Beast! Today is Day {crnt_strak} of hitting your DME. Keep it up. Remember....you are UNSTOPPABLE! 💪🏽"
        else:
            msg_text = "❗️ Select the DME you want to mark as completed"

        await bot.send_message(
            chat_id=group_id,
            text=f"{user_info.first_name} has completed his DME!✅ - {users_uncompleted} UNSTOPPABLES remaining for 100%",
        )
        _mark_notified_today(user_id)
        await call.answer("Group notified successfully!", show_alert=True)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=msg_text,
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Failed to notify group: {e}")
