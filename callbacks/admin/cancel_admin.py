from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import get_admin_menu

router = Router()


@router.callback_query(F.data == "cancel_admin")
async def end_cancel_admin(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await state.clear()

    await bot.delete_message(user_id, call.message.message_id)

    await bot.send_message(
        chat_id=user_id,
        text="👩‍💼 You opened admin panel",
        reply_markup=await get_admin_menu(),
    )
