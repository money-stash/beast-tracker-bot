from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext


from database.db import db
from keyboards.inline.admin import get_back_to_admin

router = Router()


@router.callback_query(F.data.startswith("ban_user_"))
async def start_ban_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_user = call.data.split("ban_user_")[-1]
    is_user = await db.find_user(picked_user)

    kb = [
        [
            InlineKeyboardButton(
                text="✅ Accept", callback_data=f"accept_ban_user_{is_user.user_id}"
            )
        ],
        [InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"⁉️ Are you sure you want to ban the user?\n\n{is_user.first_name}({is_user.username})",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("accept_ban_user_"))
async def accept_ban_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_user = call.data.split("accept_ban_user_")[-1]
    await db.ban_user(picked_user, True)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="🥳 User was succussully banned!",
        reply_markup=await get_back_to_admin(),
    )
