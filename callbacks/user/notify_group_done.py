from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
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
    user_info = await db.get_user(user_id)
    users_uncompleted = await db.count_users_not_completed_all_tasks_today()

    group_id = get_group_id()

    try:
        await bot.send_message(
            chat_id=group_id,
            text=f"{user_info.first_name} has completed his DME!✅ - {users_uncompleted} UNSTOPPABLES remaining for 100%",
        )
        await call.answer("Group notified successfully!", show_alert=True)
    except Exception as e:
        logger.error(f"Failed to notify group: {e}")
        # await call.answer("Failed to notify group. Please try again later.", show_alert=True)
