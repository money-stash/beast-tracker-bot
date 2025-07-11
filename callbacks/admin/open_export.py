from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from database.db import db
from utils.json_utils import get_group_id
from keyboards.inline.admin import get_group_settings_menu

router = Router()


@router.callback_query(F.data == "open_export")
async def open_open_export(call: CallbackQuery, bot: Bot, user_id: int):
    group_id = get_group_id()

    file_path = await db.export_all_users_report()

    file = FSInputFile(file_path)
    await bot.send_document(chat_id=user_id, document=file)
