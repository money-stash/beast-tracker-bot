from pytz import timezone
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import db
from states.admin import SetNewRotationDate
from keyboards.inline.admin import get_back_to_admin, get_cancel_admin
from utils.json_utils import get_next_rotation, update_next_rotation

router = Router()


@router.callback_query(F.data == "set_partners_auto_rotation")
async def start_set_next_rotation_date(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.set_state(SetNewRotationDate.next_rotation_date)

    current_rotation = get_next_rotation()
    await bot.edit_message_text(
        chat_id=user_id,
        text=f"Current rotation date is: {current_rotation}\nPlease send the new rotation date in the format DD-MM-YYYY(for example: 01.11.2026).",
        reply_markup=await get_cancel_admin(),
        message_id=call.message.message_id,
    )

    await state.update_data({"msg_id": call.message.message_id})


@router.message(SetNewRotationDate.next_rotation_date, F.text)
async def set_next_rotation_date(
    message: Message, bot: Bot, state: FSMContext, user_id: int
):
    data = await state.get_data()
    try:
        new_date = datetime.strptime(message.text, "%d.%m.%Y")
        new_date = new_date.astimezone(timezone("US/Eastern")).strftime("%d-%m-%Y")

        update_next_rotation(new_date)
        await bot.edit_message_text(
            chat_id=user_id,
            text=f"Next rotation date successfully updated to: {new_date}",
            reply_markup=await get_back_to_admin(),
            message_id=data["msg_id"],
        )
    except ValueError:
        await bot.edit_message_text(
            chat_id=user_id,
            text="Invalid date format. Please use DD.MM.YYYY (e.g., 01.11.2026).",
            reply_markup=await get_cancel_admin(),
            message_id=data["msg_id"],
        )
        return

    await state.clear()
