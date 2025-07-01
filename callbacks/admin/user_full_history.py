from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database.db import db

router = Router()


@router.callback_query(F.data.startswith("user_full_history_"))
async def send_file_user_full_history(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_id = call.data.split("user_full_history_")[-1]
    file = await db.export_user_daily_history(picked_id)

    doc = FSInputFile(file)

    await bot.send_document(user_id, doc)
