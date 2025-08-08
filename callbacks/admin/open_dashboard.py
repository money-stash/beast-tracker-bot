from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from utils.json_utils import get_group_id
from keyboards.inline.admin import get_back_to_admin

router = Router()


@router.callback_query(F.data == "open_dashboard")
async def print_open_dashboard(call: CallbackQuery, bot: Bot, user_id: int):
    group_id = get_group_id()

    if group_id != "none":
        chat = await bot.get_chat(group_id)
        members_count = len(await db.get_users())

        max_streak = await db.get_user_with_longest_daily_streak()

        text = f"📊 You opened <b>Dashboard Overview</b>\n\n"
        text += f"👥 Total users: {members_count}\n"
        completed_all_tasks_today = await db.count_users_completed_all_tasks_today()
        total_users = len(await db.get_users())
        percentage = (
            (completed_all_tasks_today / members_count * 100) if total_users else 0
        )
        text += f"✅ All completed: {completed_all_tasks_today} ({percentage:.0f}%)\n"
        text += f"Longest active streak: <b>{max_streak['max_streak']} days </b> ({max_streak['user_id']} @{max_streak['username']})"

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=await get_back_to_admin(),
        )
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text="Fristly, you need add group",
            reply_markup=await get_back_to_admin(),
        )
