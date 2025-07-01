from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


from database.db import db
from states.admin import FindUserMem
from keyboards.inline.admin import get_back_to_admin, get_mem_user_menu

router = Router()


@router.callback_query(F.data == "open_mem_directory")
async def open_mem_directory(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="🦋 You opened <b>Member Directory</b> menu\n\nPls write user: @username, link or user_id",
        reply_markup=await get_back_to_admin(),
    )

    await state.update_data({"msg_id": call.message.message_id})
    await state.set_state(FindUserMem.user_identy)


@router.message(FindUserMem.user_identy)
async def end_find_user_mem(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    user_identy = msg.text
    is_user = await db.find_user(user_identy)

    await bot.delete_message(user_id, msg.message_id)
    user_streak = await db.get_current_daily_streak(is_user.user_id)
    max_streak = await db.get_user_with_longest_daily_streak(is_user.user_id)
    missed_days = await db.get_missed_daily_days(is_user.user_id)

    if is_user:
        info = "<b>👤 USER INFO</b>\n\n"
        info += f"User_id: <code>{is_user.user_id}</code>\n"
        info += f"Username: <code>{is_user.username}</code>\n"
        info += f"First name: <code>{is_user.first_name}</code>\n"
        info += f"Reg date: <code>{is_user.reg_date}</code>\n"
        info += f"Current DME streak: <code>{user_streak}</code>\n"
        info += f"All-time streak high: <code>{max_streak['max_streak']}</code>\n"
        info += f"Total missed days: <code>{missed_days}</code>\n"

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=info,
            reply_markup=await get_mem_user_menu(is_user.user_id),
        )
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="🚨 I can't find a user by that ID.\nTry write again",
        )
