import re
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin import ChangeDME
from keyboards.inline.admin import get_cancel_admin, get_back_to_admin
from utils.json_utils import get_dme_hours, update_dme_hours

router = Router()


@router.callback_query(F.data == "set_dme_hours")
async def start_change_dme(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"Old dme check hours: <code>{get_dme_hours()}</code>\nEnter new hours(for example: 00:05-22:30):",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(ChangeDME.new_dme)
    await state.update_data({"msg_id": call.message.message_id})


@router.message(ChangeDME.new_dme, F.text)
async def change_dme_hours(message: Message, state: FSMContext, user_id: int, bot: Bot):
    new_dme = message.text.strip()
    data = await state.get_data()
    msg_id = data.get("msg_id")

    await bot.delete_message(chat_id=user_id, message_id=msg_id)

    # Проверка формата времени: HH:MM-HH:MM
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d-(?:[01]\d|2[0-3]):[0-5]\d$"
    if not new_dme or not re.match(pattern, new_dme):
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_id,
            text="Invalid time format. Please enter a time range like: 00:05-22:30",
        )
        return

    update_dme_hours(new_dme)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=f"🥳 DME check hours updated to: <code>{new_dme}</code>",
        reply_markup=await get_back_to_admin(),
    )

    await state.clear()
