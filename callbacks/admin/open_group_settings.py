from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from utils.json_utils import get_group_id
from keyboards.inline.admin import get_group_settings_menu

router = Router()


@router.callback_query(F.data == "open_group_settings")
async def open_admion_menu(call: CallbackQuery, bot: Bot, user_id: int):
    group_id = get_group_id()

    text = f"👩‍💼 You opened group settings\n"
    if group_id != "none":
        chat = await bot.get_chat(group_id)
        members_count = await bot.get_chat_member_count(group_id)
        group_title = chat.title
        text += f"📛 Group name: {group_title}\n👥 Members count: {members_count}"
    else:
        text = "🚨 Firstly, add group for using bot\nClick '<b>🔄 Change group</b>'"

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=await get_group_settings_menu(),
    )
