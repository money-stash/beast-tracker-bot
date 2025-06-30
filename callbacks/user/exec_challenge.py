from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db import db

router = Router()


@router.callback_query(F.data.startswith("non_exec_challenge_"))
async def set_non_exec_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenge_id = call.data.split("non_exec_challenge_")[-1]
    await db.upsert_challenge_history(challenge_id, user_id, executed=False)

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
                text="🔙 Back",
                callback_data=f"user_challenges",
            )
        ],
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_reply_markup(
        chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("exec_challenge_"))
async def set_exec_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    challenge_id = call.data.split("exec_challenge_")[-1]
    await db.upsert_challenge_history(challenge_id, user_id, executed=True)

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
                text="🔙 Back",
                callback_data=f"user_challenges",
            )
        ],
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_reply_markup(
        chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboard
    )
