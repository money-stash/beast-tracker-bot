from aiogram import Router, F, Bot
from aiogram.types import Message

from database.db import db

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot, user_id: int):
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    await db.create_user(user_id, first_name, username)

    await msg.answer(
        text=f"👋 Hi, <b>{msg.from_user.full_name}</b>",
        parse_mode="html",
    )
