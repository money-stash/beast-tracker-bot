from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db import db
from keyboards.inline.admin import get_challenges_menu
from utils.json_utils import get_group_id, update_group_id

router = Router()


@router.callback_query(F.data == "open_challenges_control")
async def print_open_challenges_control(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenges = await db.get_all_challenges()
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="🎯 You opened <b>MINI CHALLANGES</b> menu",
        reply_markup=await get_challenges_menu(challenges),
    )
