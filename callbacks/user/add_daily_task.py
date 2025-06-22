from pytz import timezone
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import db
from states.user import AddDailyTask
from keyboards.inline.user import get_accept_cancel_keyboard, get_back_to_daily_menu

router = Router()


@router.callback_query(F.data == "add_daily_task")
async def add_daily_task(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.delete()

    msg = await bot.send_message(
        chat_id=call.from_user.id,
        text="✏️ Enter the text of the daily task",
    )

    await state.update_data({"msg_id": msg.message_id})
    await state.set_state(AddDailyTask.waiting_for_task_text)


@router.message(AddDailyTask.waiting_for_task_text)
async def process_task_text(message: Message, state: FSMContext, bot: Bot):
    task_text = message.text
    data = await state.get_data()

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )

    await state.update_data(task_text=task_text)

    await bot.edit_message_text(
        text=f"✅ You've entered the text of the assignment:\n\n<b>{task_text}</b>\n\n❓ You want to keep it?",
        chat_id=message.from_user.id,
        message_id=data.get("msg_id"),
        reply_markup=await get_accept_cancel_keyboard(),
        parse_mode="HTML",
    )

    await state.set_state(AddDailyTask.waiting_for_accept)


@router.callback_query(
    AddDailyTask.waiting_for_accept,
    F.data.in_({"accept", "cancel"}),
)
async def process_accept_cancel(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    task_text = user_data.get("task_text")

    if call.data == "accept":
        user_id = call.from_user.id
        now_date = datetime.now(timezone("Europe/Kyiv")).strftime("%Y.%m.%d")

        await db.create_daily_task(user_id=user_id, task_text=task_text, date=now_date)

        await bot.edit_message_text(
            text="✅ You have successfully added a task",
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=await get_back_to_daily_menu(),
        )

    else:
        await bot.edit_message_text(
            text="❌ You canceled adding a task",
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=await get_back_to_daily_menu(),
        )

    await state.clear()
