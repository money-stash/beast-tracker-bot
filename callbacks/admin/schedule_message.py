from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    FSInputFile,
)
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from database.db import db
from utils.sched_msgs import send_schedul_msg
from states.admin import ScheduleMessage
from keyboards.inline.admin import get_back_to_admin, get_cancel_admin

from config import scheduler, us_tz

router = Router()


@router.callback_query(F.data == "schedule_message")
async def start_send_schehedule_msg(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):

    kb = [
        [InlineKeyboardButton(text="Text", callback_data="format_text")],
        [InlineKeyboardButton(text="Photo", callback_data="format_photo")],
        [InlineKeyboardButton(text="Video", callback_data="format_video")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="💚 Choose message format",
        reply_markup=keyboard,
    )
    await state.set_state(ScheduleMessage.pick_format)


@router.callback_query(ScheduleMessage.pick_format)
async def get_message_format(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    cdata = call.data
    if cdata.startswith("format_"):
        picked_format = cdata.split("format_")[-1]
        await state.update_data({"picked_format": picked_format})

        if picked_format == "text":
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="✏️ Send text for message",
                reply_markup=await get_cancel_admin(),
            )

            await state.set_state(ScheduleMessage.format_text)
            await state.update_data(
                {"msg_id": call.message.message_id, "media": "None"}
            )
        else:
            await state.set_state(ScheduleMessage.media)

            await bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="📷 Send media for message",
                reply_markup=await get_cancel_admin(),
            )

            await state.update_data(
                {"msg_id": call.message.message_id, "media": "None"}
            )


@router.message(ScheduleMessage.media)
async def get_media_for_message(
    msg: Message, bot: Bot, state: FSMContext, user_id: int
):
    media = None
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)

    if msg.photo:
        file_obj = msg.photo[-1]
        ext = ".jpg"
    elif msg.video:
        file_obj = msg.video
        ext = ".mp4"
    else:
        await msg.answer("❌ send photo or video.")
        return

    file_id = file_obj.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = f"{file_id}{ext}"
    dest = downloads_dir / filename

    await bot.download_file(file_path, destination=dest)

    await state.update_data({"media": str(dest)})

    await bot.delete_message(user_id, msg.message_id)
    data = await state.get_data()

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="✏️ Send text for message",
        reply_markup=await get_cancel_admin(),
    )
    await state.set_state(ScheduleMessage.format_text)


@router.message(ScheduleMessage.format_text)
async def get_msg_caption(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    data = await state.get_data()
    msg_text = msg.text

    await bot.delete_message(user_id, msg.message_id)

    await state.update_data({"msg_text": msg_text})

    kb = [
        [InlineKeyboardButton(text="Every day", callback_data="every_day")],
        [InlineKeyboardButton(text="Every week", callback_data="every_week")],
        [InlineKeyboardButton(text="One time", callback_data="one_time")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="🕰️ Pick repeat or one time",
        reply_markup=keyboard,
    )

    await state.set_state(ScheduleMessage.repeat)


@router.callback_query(ScheduleMessage.repeat)
async def get_msg_repeat(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_repeat = call.data
    data = await state.get_data()

    await state.update_data({"picked_repeat": picked_repeat})

    kb = []
    hour = 6
    while hour <= 20:
        row = []
        row.append(
            InlineKeyboardButton(text=f"{hour}:00", callback_data=f"time_{hour}:00")
        )
        if hour < 20:
            row.append(
                InlineKeyboardButton(text=f"{hour}:30", callback_data=f"time_{hour}:30")
            )
        kb.append(row)
        hour += 1

    kb.append(
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    if picked_repeat == "one_time":
        await state.set_state(ScheduleMessage.date)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="📅 Write date for message, format: DD.MM.YYYY\nFor example: 23.10.2025",
            reply_markup=await get_cancel_admin(),
        )

    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="🕰️ Pick time for scheduled message",
            reply_markup=keyboard,
        )
        await state.set_state(ScheduleMessage.time)


@router.message(ScheduleMessage.date)
async def get_one_time_date(msg: Message, bot: Bot, state: FSMContext, user_id: int):
    date = msg.text
    data = await state.get_data()

    await bot.delete_message(user_id, msg.message_id)

    try:
        parsed_date = datetime.strptime(date, "%d.%m.%Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text="❌ Incorrect date format.\nFor example: 23.10.2025",
            reply_markup=await get_cancel_admin(),
        )
        return

    await state.update_data({"one_time_date": formatted_date})

    data = await state.get_data()

    kb = []
    hour = 6
    while hour <= 20:
        row = []
        row.append(
            InlineKeyboardButton(text=f"{hour}:00", callback_data=f"time_{hour}:00")
        )
        if hour < 20:
            row.append(
                InlineKeyboardButton(text=f"{hour}:30", callback_data=f"time_{hour}:30")
            )
        kb.append(row)
        hour += 1

    kb.append(
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.edit_message_text(
        chat_id=user_id,
        message_id=data["msg_id"],
        text="🕰️ Pick time for scheduled message",
        reply_markup=keyboard,
    )

    await state.set_state(ScheduleMessage.time)


@router.callback_query(ScheduleMessage.time)
async def get_scheduled_time(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    picked_time = call.data.split("time_")[-1]
    await state.update_data({"picked_time": picked_time})

    data = await state.get_data()

    msg_text = "SCHEDULED MESSAGE DATA\n\n"

    msg_text += f"repeat: {data['picked_repeat']}\n"
    msg_text += f"media: {data['media']}\n"
    msg_text += f"text: {data['msg_text']}\n"
    msg_text += f"time: {data['picked_time']}\n"
    if data["picked_repeat"] == "one_time":
        msg_text += f"date:  {data['one_time_date']}"

    kb = [
        [
            InlineKeyboardButton(text="✅ Accept", callback_data="accept_scheduled"),
        ],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    if data["media"] == "None":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data["msg_id"],
            text=msg_text,
            reply_markup=keyboard,
        )
    else:
        media_path = Path(data["media"])

        await bot.delete_message(user_id, data["msg_id"])

        media_file = FSInputFile(media_path)
        if media_path.suffix.lower() == ".mp4":
            await bot.send_video(
                chat_id=user_id,
                video=media_file,
                caption=msg_text,
                reply_markup=keyboard,
            )
        else:
            await bot.send_photo(
                chat_id=user_id,
                photo=media_file,
                caption=msg_text,
                reply_markup=keyboard,
            )

    await state.set_state(ScheduleMessage.accept)


@router.callback_query(ScheduleMessage.accept)
async def end_send_schedule(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    if call.data == "accept_scheduled":
        data = await state.get_data()
        if "one_time_date" not in data:
            data["one_time_date"] = data["picked_repeat"]

        msg_info = await db.add_schedule_message(
            text=data["msg_text"],
            media_path=data["media"],
            date=str(data["one_time_date"]),
            time=data["picked_time"],
            repeat=data["picked_repeat"],
        )

        job_args = [bot, msg_info.id]

        if data["picked_repeat"] == "every_day":
            scheduler.add_job(
                send_schedul_msg,
                CronTrigger(
                    hour=int(data["picked_time"].split(":")[0]),
                    minute=int(data["picked_time"].split(":")[1]),
                    timezone=us_tz,
                ),
                args=job_args,
            )

        elif data["picked_repeat"] == "every_week":
            scheduler.add_job(
                send_schedul_msg,
                CronTrigger(
                    day_of_week=datetime.now(us_tz).strftime("%a").lower(),
                    hour=int(data["picked_time"].split(":")[0]),
                    minute=int(data["picked_time"].split(":")[1]),
                    timezone=us_tz,
                ),
                args=job_args,
            )

        elif data["picked_repeat"] == "one_time":
            date_parts = [int(p) for p in str(data["one_time_date"]).split("-")]
            time_parts = [int(p) for p in data["picked_time"].split(":")]

            scheduler.add_job(
                send_schedul_msg,
                trigger="date",
                run_date=datetime(
                    date_parts[0],
                    date_parts[1],
                    date_parts[2],
                    time_parts[0],
                    time_parts[1],
                    tzinfo=us_tz,
                ),
                args=job_args,
            )

        await bot.delete_message(user_id, call.message.message_id)

        await bot.send_message(
            chat_id=user_id,
            text="✅ New scheduled message successfully added!",
            reply_markup=await get_back_to_admin(),
        )

        await state.clear()
