from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import db
from keyboards.inline.admin import get_back_to_admin
from utils.json_utils import get_rot_freq

router = Router()


@router.callback_query(F.data == "reload_partners")
async def start_reload_partners(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    kb = [
        [
            InlineKeyboardButton(
                text="✅ Yes, reassign pairs",
                callback_data="accept_reload_partners",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ No, cancel",
                callback_data="cancel_admin",
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="⁉️ Are you sure you want to reassign pairs for all users?",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "accept_reload_partners")
async def accept_reload_partners(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    rot_freq = get_rot_freq()

    await db.assign_random_partners()

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="✅ All users have been reassigned pairs.",
        reply_markup=get_back_to_admin(),
    )

    await state.clear()
