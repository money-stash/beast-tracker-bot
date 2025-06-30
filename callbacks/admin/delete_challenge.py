from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import db
from keyboards.inline.admin import get_back_to_admin

router = Router()


@router.callback_query(F.data.startswith("delete_challenge_"))
async def print_start_del_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenge_id = call.data.split("delete_challenge_")[-1]
    challenge_info = await db.get_challenge_by_id(challenge_id)

    kb = [
        [
            InlineKeyboardButton(
                text="✅ Accept",
                callback_data=f"accept_del_challenge_{challenge_info.id}",
            )
        ],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"⁉️ Are you sure you want to delete <b>{challenge_info.name}</b> challenge?",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("accept_del_challenge_"))
async def end_del_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenge_id = call.data.split("accept_del_challenge_")[-1]
    challenge_info = await db.get_challenge_by_id(challenge_id)
    await db.delete_challenge(challenge_id)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"🥳 Challenge <b>{challenge_info.name}</b> was successfully deleted!",
        reply_markup=await get_back_to_admin(),
    )
