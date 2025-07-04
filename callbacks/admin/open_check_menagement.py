from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import check_menagement_menu

router = Router()


@router.callback_query(F.data == "open_check_menagement")
async def print_check_menagement(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="📫 You opened <b>Check-In Management</b> menu",
        reply_markup=await check_menagement_menu(),
    )
