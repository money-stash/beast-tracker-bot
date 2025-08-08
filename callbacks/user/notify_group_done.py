from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

from database.db import db
from utils.logger import logger
from utils.json_utils import get_group_id

router = Router()


@router.callback_query(F.data == "notify_group_dme_done")
async def notify_group_dme_done(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    user_id = call.from_user.id
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
        await call.answer("Group notified successfully!", show_alert=True)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=msg_text,
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Failed to notify group: {e}")
        # await call.answer(
        #     "Failed to notify group. Please try again later.", show_alert=True
        # )
