from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin import ChangeGroup
from keyboards.inline.admin import get_back_to_admin, get_cancel_admin
from utils.json_utils import get_group_id, update_group_id

router = Router()


@router.callback_query(F.data == "change_group")
async def start_change_group(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"First open the bot @getmy_idbot and get your group id.\nOld group_id: <code>{get_group_id()}</code>\nEnter new group id",
        reply_markup=await get_cancel_admin(),
    )
    await state.update_data({"msg_id": call.message.message_id})
    await state.set_state(ChangeGroup.new_group_id)


@router.message(ChangeGroup.new_group_id)
async def end_change_group(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    new_group_id = msg.text

    await bot.delete_message(message_id=msg.message_id, chat_id=user_id)

    if not new_group_id.startswith("-") or not new_group_id[1:].isdigit():
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="❌ Group id must be a negative number\ntry write again",
        )
        return

    try:
        chat = await bot.get_chat(new_group_id)
        members_count = await bot.get_chat_member_count(new_group_id)

        update_group_id(new_group_id)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=f"✅ Group id is updated!\n👥 Members count: {members_count}",
            reply_markup=await get_back_to_admin(),
        )
    except Exception as e:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=f"❌ failed to access group\n{e}\ntry write again",
            reply_markup=await get_cancel_admin(),
        )
        return
