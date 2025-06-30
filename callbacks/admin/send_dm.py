from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import db
from states.admin import SendDmAdmin
from keyboards.inline.admin import get_back_to_admin, get_cancel_admin

router = Router()


@router.callback_query(F.data.startswith("send_manual_message_"))
async def start_send_dm_to_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_id = call.data.split("send_manual_message_")[-1]
    is_user = await db.find_user(picked_id)

    await state.update_data({"msg_id": call.message.message_id})
    await state.update_data({"user_dm_id": picked_id})

    await state.set_state(SendDmAdmin.message_text)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"✏️ Write message text for user {is_user.first_name}({is_user.username})",
        reply_markup=await get_cancel_admin(),
    )


@router.callback_query(F.data == "send_dm")
async def start_send_dm(call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="👤 Send user identifier: username, link or user_id",
        reply_markup=await get_cancel_admin(),
    )
    await state.update_data({"msg_id": call.message.message_id})
    await state.set_state(SendDmAdmin.user_identy)


@router.message(SendDmAdmin.user_identy)
async def get_user_identy_dm(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    user_identy = msg.text
    is_user = await db.find_user(user_identy)

    await bot.delete_message(user_id, msg.message_id)

    if is_user:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=f"✏️ Write message text for user {is_user.first_name}({is_user.username})",
            reply_markup=await get_cancel_admin(),
        )
        await state.set_state(SendDmAdmin.message_text)
        await state.update_data({"user_dm_id": is_user.user_id})
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=f"❌ Can't find user, try again!",
            reply_markup=await get_cancel_admin(),
        )


@router.message(SendDmAdmin.message_text)
async def end_send_db_admin(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    msg_text = msg.text

    try:
        await bot.send_message(chat_id=data["user_dm_id"], text=msg_text)
    except Exception as ex:
        print(f"ERROR WHILE SENDING DM TO USER: {ex}")

    await bot.delete_message(user_id, msg.message_id)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="🥳 Message was successfully sended to user!",
        reply_markup=await get_back_to_admin(),
    )

    await state.clear()
