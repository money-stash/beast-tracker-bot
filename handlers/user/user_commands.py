from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType

from database.db import db
from middlewares.user import get_main_menu
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/start", F.chat.type == ChatType.PRIVATE)
async def start_private(msg: Message, bot: Bot, user_id: int):
    first_name = msg.from_user.first_name
    username = msg.from_user.username
    last_name = msg.from_user.last_name

    await db.create_user(
        user_id=user_id, first_name=first_name, username=username, last_name=last_name
    )

    if user_id in ADMIN_ID:
        kb = await get_main_menu(is_admin=True)
    else:
        kb = await get_main_menu()

    await msg.answer(
        text=f"👋 Hi, <b>{msg.from_user.full_name}</b>",
        parse_mode="html",
        reply_markup=kb,
    )


@router.message(
    F.text == "/start", F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})
)
async def start_group(msg: Message):
    await msg.answer(
        "Hey there Unstoppable! To get started with the bot, follow these instructions:\n"
        "1. Send a DM to the bot at: @myDMEbot\n"
        "2. Send the first message as: /start\n"
        "3. To add a DME: click DME -> +DME -> write your DME.\n\n"
        "Everyday, once you complete your DME, go to your DM with the bot, and let it know you did it:\n"
        "click DME -> Mark DME Completed for Today. When you get the Green Checkmark ✅, then click -> Notify Group.\n"
        "That will send us all a message in the group chat, so we all know you have completed your DME for the day.\n\n"
        "The bot will check in with you throughout the day to remind/ask you if you have completed your DME. "
        "Please make sure you have your notifications for that DM chat, and our group chat ON, so that the reminder "
        "work to help you on this journey. 😊"
    )
