from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import db

router = Router()


@router.callback_query(F.data.startswith("open_user_challenge_"))
async def print_user_challenge_info(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenge_id = call.data.split("open_user_challenge_")[-1]
    challenge_info = await db.get_challenge_by_id(challenge_id)

    is_executed = await db.is_challenge_executed_today(challenge_id, user_id)

    kb = []

    if is_executed:
        kb.append(
            [
                InlineKeyboardButton(
                    text="✅ Executed",
                    callback_data=f"non_exec_challenge_{challenge_id}",
                )
            ]
        )
    else:
        kb.append(
            [
                InlineKeyboardButton(
                    text="❌ Non executed",
                    callback_data=f"exec_challenge_{challenge_id}",
                )
            ]
        )

    kb.append(
        [
            InlineKeyboardButton(
                text="📊 Stats", callback_data=f"challenge_stats_{challenge_id}"
            ),
        ]
    )

    kb.append(
        [
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"user_challenges",
            )
        ],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    msg_text = f"🦋 You opened {challenge_info.name} challenge\n\n"
    msg_text += f"🏋️‍♀️ Action: <b>{challenge_info.action}</b>\n\n"
    msg_text += f"📏 Rules: <b>{challenge_info.rules}</b>\n\n"
    msg_text += f"⏰ Duration(days): <b>{challenge_info.duration}</b>\n\n"

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=msg_text,
        reply_markup=keyboard,
    )
