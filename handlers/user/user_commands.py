from aiogram import Router, F
from aiogram.types import Message

from database.db import db
from config import DB_PATH

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message):
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    await db.create_user(user_id, first_name, username)

    await msg.answer(
        text=f"👋 Hi, <b>{msg.from_user.full_name}</b>",
        parse_mode="html",
    )
