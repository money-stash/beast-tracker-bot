from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import db

from keyboards.inline.admin import get_back_to_admin

router = Router()


@router.callback_query(F.data == "open_leaderboard")
async def print_leader_bodr(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    leaderboard = await db.get_leaderboard()
    max_broke_streak = await db.get_biggest_comeback()
    max_consistent_this_month = await db.get_most_consistent_this_month()

    msg_text = "🥇 <b>LEADER bord</b>\n\n"

    msg_text += "<b>top streaks:</b>\n"
    if leaderboard:
        for i, entry in enumerate(leaderboard, 1):
            msg_text += f"{i}. user_id: {entry.user_id}, streak: {entry.streak}\n"
    else:
        msg_text += "no data\n"

    msg_text += "\n<b>biggest comeback:</b>\n"
    if max_broke_streak:
        msg_text += (
            f"user_id: {max_broke_streak['user_id']}, "
            f"gap: {max_broke_streak['max_gap']} days, "
            f"comeback streak: {max_broke_streak['comeback_streak']}\n"
        )
    else:
        msg_text += "no data\n"

    msg_text += "\n<b>most consistent this month:</b>\n"
    if max_consistent_this_month:
        msg_text += (
            f"user_id: {max_consistent_this_month['user_id']}, "
            f"first_name: {max_consistent_this_month['first_name']}, "
            f"username: @{max_consistent_this_month['username']}, "
            f"done days: {max_consistent_this_month['done_days']}\n"
        )
    else:
        msg_text += "no data\n"

    await call.message.edit_text(
        msg_text, parse_mode="html", reply_markup=await get_back_to_admin()
    )
    await call.answer()
