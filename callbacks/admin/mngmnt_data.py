from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext


from database.db import db
from keyboards.inline.admin import get_admin_menu

router = Router()


@router.callback_query(F.data == "mngmnt_data")
async def open_mngmnt_data_info(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    mngmnt_data_file = await db.export_checkin_report()
    file = FSInputFile(mngmnt_data_file)

    await bot.send_document(
        chat_id=user_id,
        document=file,
        caption="Here is the management data report.",
        reply_markup=await get_admin_menu(),
    )
