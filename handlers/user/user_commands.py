from aiogram import Router, F, Bot
from aiogram.types import Message

from database.db import db
from middlewares.user import get_main_menu
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot, user_id: int):
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    await db.create_user(user_id, first_name, username)

    if user_id == ADMIN_ID:
        kb = await get_main_menu(is_admin=True)
    else:
        kb = await get_main_menu()

    await msg.answer(
        text=f"👋 Hi, <b>{msg.from_user.full_name}</b>",
        parse_mode="html",
        reply_markup=kb,
    )
