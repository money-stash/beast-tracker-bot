from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db import db
from keyboards.inline.user import get_challenges_menu

router = Router()


@router.callback_query(F.data == "user_challenges")
async def print_user_challenges(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenges = await db.get_all_challenges()
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="🎯 You opened <b>MINI CHALLANGES</b> menu",
        reply_markup=await get_challenges_menu(challenges),
    )
