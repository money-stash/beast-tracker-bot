from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import get_admin_settings_menu

router = Router()


@router.callback_query(F.data == "open_settings")
async def print_admin_settings(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="⚙️ You opened <b>ADMIN SETTINGS</b> menu",
        reply_markup=await get_admin_settings_menu(),
    )
