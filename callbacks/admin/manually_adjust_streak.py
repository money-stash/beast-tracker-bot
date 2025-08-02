from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from database.db import db
from states.admin import ChangeStreak
from keyboards.inline.admin import get_back_to_admin, get_cancel_admin

router = Router()


@router.callback_query(F.data.startswith("manually_adjust_streak_"))
async def start_change_streak(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_userid = call.data.split("manually_adjust_streak_")[-1]

    current_streak = await db.get_current_daily_streak(picked_userid)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"Current daily streak: {current_streak}\nWrite new streak for this user",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(ChangeStreak.new_streak)
    await state.update_data(
        {"picked_userid": picked_userid, "msg_id": call.message.message_id}
    )


@router.message(ChangeStreak.new_streak)
async def end_change_streak(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    new_streak = msg.text

    await bot.delete_message(user_id, msg.message_id)

    if new_streak.isdigit():
        await db.set_user_streak(
            user_id=data["picked_userid"], target_streak=int(new_streak)
        )

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="🥳 User streak successufully changed!",
            reply_markup=await get_back_to_admin(),
        )

        await state.clear()
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="❌ WRITE NUMBER!",
        )
