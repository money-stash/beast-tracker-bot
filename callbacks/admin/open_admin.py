from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import get_admin_menu

router = Router()


@router.callback_query(F.data == "open_admin")
async def open_admion_menu(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.clear()
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="👩‍💼 You opened admin panel",
        reply_markup=await get_admin_menu(),
    )


@router.callback_query(F.data == "back_to_admin")
async def open_back_to_admin(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.clear()
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="👩‍💼 You opened admin panel",
        reply_markup=await get_admin_menu(),
    )
