from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import get_partner_menager

router = Router()


@router.callback_query(F.data == "open_partner_manager")
async def print_partner_manager(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="👥 You opened <b>PARTNERS MANAGER</b> menu",
        reply_markup=await get_partner_menager(),
    )
