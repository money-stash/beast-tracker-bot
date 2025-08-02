from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from database.db import db

from config import DB_PATH, DATA_JSON


router = Router()


@router.callback_query(F.data == "open_export")
async def open_open_export(call: CallbackQuery, bot: Bot, user_id: int):
    file_path = await db.export_all_users_report()

    file = FSInputFile(file_path)
    await bot.send_document(chat_id=user_id, document=file)

    db_file = FSInputFile(DB_PATH)
    data_file = FSInputFile(DATA_JSON)

    try:
        await bot.send_document(
            chat_id=user_id,
            document=db_file,
            caption="Here is the database file.",
        )
    except Exception as e:
        print(f"Error while sending database file to admin {user_id}: {e}")

    try:
        await bot.send_document(
            chat_id=user_id,
            document=data_file,
            caption="Here is the data file.",
        )
    except Exception as e:
        print(f"Error while sending data file to admin {user_id}: {e}")
