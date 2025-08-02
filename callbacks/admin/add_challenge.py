from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database.db import db
from states.admin import NewChallenge
from keyboards.inline.admin import get_cancel_admin, get_back_to_admin

router = Router()


@router.callback_query(F.data == "add_new_challenge")
async def start_add_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Write name for new CHALLENGE",
        reply_markup=await get_cancel_admin(),
    )
    await state.update_data({"msg_id": call.message.message_id})
    await state.set_state(NewChallenge.name)


@router.message(NewChallenge.name)
async def get_challenge_name(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    name = msg.text
    await state.update_data({"name": name})
    await bot.delete_message(user_id, msg.message_id)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="Write action for new CHALLENGE",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(NewChallenge.action)


@router.message(NewChallenge.action)
async def get_challenge_action(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    action = msg.text
    await state.update_data({"action": action})
    await bot.delete_message(user_id, msg.message_id)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="Write rules for new CHALLENGE",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(NewChallenge.rules)


@router.message(NewChallenge.rules)
async def get_challenge_rules(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    rules = msg.text
    await state.update_data({"rules": rules})
    await bot.delete_message(user_id, msg.message_id)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="Write duration for new CHALLENGE",
        reply_markup=await get_cancel_admin(),
    )

    await state.set_state(NewChallenge.duration)


@router.message(NewChallenge.duration)
async def get_challenge_duration(
    msg: Message, bot: Bot, state: FSMContext, user_id: int
):
    data = await state.get_data()
    duration = msg.text
    await state.update_data({"duration": duration})
    await bot.delete_message(user_id, msg.message_id)

    msg_text = "🥳 NEW CHALLANGE:\n\n"
    msg_text += f"name: {data['name']}\n"
    msg_text += f"action: {data['action']}\n"
    msg_text += f"rules: {data['rules']}\n"
    msg_text += f"duration: {duration}\n"

    kb = [
        [InlineKeyboardButton(text="✅ Accept", callback_data="accept_new_challenge")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text=msg_text,
        reply_markup=keyboard,
    )

    await state.set_state(NewChallenge.accept)


@router.callback_query(F.data == "accept_new_challenge")
async def end_add_challenge(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    data = await state.get_data()

    await db.add_challenge(
        name=data["name"],
        duration=data["duration"],
        rules=data["rules"],
        action=data["action"],
    )

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="New challenge was successfully added!",
        reply_markup=await get_back_to_admin(),
    )

    await state.clear()
