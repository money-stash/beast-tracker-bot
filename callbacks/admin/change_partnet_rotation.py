from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin import RotFreq
from keyboards.inline.admin import get_cancel_admin, get_back_to_admin
from utils.json_utils import get_rot_freq, update_rot_freq

router = Router()


@router.callback_query(F.data == "change_partnet_rotation")
async def start_change_rotation(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"Old rotation partner frequency: <code>{get_rot_freq()}</code> days\nEnter new frequency(in days)",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(RotFreq.new_freq)
    await state.update_data({"msg_id": call.message.message_id})


@router.message(RotFreq.new_freq)
async def end_change_rotation(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    msg_text = msg.text

    await bot.delete_message(user_id, msg.message_id)

    if msg_text.isdigit():
        update_rot_freq(msg_text)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="✅ Partner rotation frequency was successully updated!",
            reply_markup=await get_back_to_admin(),
        )
        await state.clear()

    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="❌ New frequency must be a digit!\nTry again",
        )
