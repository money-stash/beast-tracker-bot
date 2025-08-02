from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import db
from utils.json_utils import get_permission

router = Router()


@router.callback_query(F.data.startswith("open_perm_"))
async def print_user_perm(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_user_id = int(call.data.split("_")[-1])
    current_permission = get_permission(picked_user_id)

    user_info = await db.get_user(picked_user_id)

    kb = []
    permissions = ["admin", "scheduler"]

    if current_permission:
        actual_permission = current_permission

        for perm in permissions:
            if perm == actual_permission:
                kb.append(
                    [
                        InlineKeyboardButton(
                            text=f"🗑️Delete his role",
                            callback_data=f"delete_perm_{picked_user_id}",
                        )
                    ]
                )
            else:
                kb.append(
                    [
                        InlineKeyboardButton(
                            text=f"✅Give him {perm} role",
                            callback_data=f"set_perm_{picked_user_id}_{perm}",
                        )
                    ]
                )
    else:
        for perm in permissions:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=f"✅Give him {perm} role",
                        callback_data=f"set_perm_{picked_user_id}_{perm}",
                    )
                ]
            )

    kb.append(
        [
            InlineKeyboardButton(
                text="🔙 Back to permissions",
                callback_data=f"open_admin_permission",
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        text=f"👤 {user_info.first_name} has {current_permission if current_permission else 'no'} role",
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )
