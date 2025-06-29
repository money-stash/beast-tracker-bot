from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import get_daily_motivation_menu

router = Router()


@router.callback_query(F.data == "open_motivation")
async def print_admin_daily_motivation(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="🏋️‍♀️ You opened <b>DAILY MOTIVATION</b> menu",
        reply_markup=await get_daily_motivation_menu(),
    )
