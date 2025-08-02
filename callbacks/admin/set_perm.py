from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import db
from utils.json_utils import (
    get_permission,
    update_permission,
    add_permission,
    remove_permission,
)
from keyboards.inline.admin import get_back_to_admin

router = Router()


@router.callback_query(F.data.startswith("set_perm_"))
async def set_user_permission(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    data = call.data.split("_")
    picked_user_id = int(data[2])
    permission = data[3]

    current_permission = get_permission(picked_user_id)

    if current_permission:
        update_permission(picked_user_id, permission)
    else:
        add_permission(picked_user_id, permission)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to user",
                    callback_data=f"open_perm_{picked_user_id}",
                )
            ]
        ]
    )

    await call.message.edit_text(
        text=f"✅ Permission {permission} set for user {picked_user_id}",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("delete_perm_"))
async def remove_user_permission(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    data = call.data.split("_")
    picked_user_id = int(data[-1])

    remove_permission(picked_user_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to user",
                    callback_data=f"open_perm_{picked_user_id}",
                )
            ]
        ]
    )

    await call.message.edit_text(
        text=f"🥳 Permission removed for user {picked_user_id}",
        reply_markup=keyboard,
    )
