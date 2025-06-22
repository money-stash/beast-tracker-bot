from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "ok_daily")
async def ok_daily(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
