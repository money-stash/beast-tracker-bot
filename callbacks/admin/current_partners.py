from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import db

from keyboards.inline.admin import get_back_partners_mngr

router = Router()


@router.callback_query(F.data == "current_partners")
async def print_partners_overview(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    partners_text = await db.get_partners_overview()

    msg_text = "👥 You opened <b>PARTNERS OVERVIEW</b>\n\n"
    msg_text += partners_text

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=msg_text,
        reply_markup=await get_back_partners_mngr(),
    )
