import os
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from states.admin import UploadImageAutopost
from keyboards.inline.admin import get_cancel_admin, get_back_to_admin

router = Router()


@router.callback_query(F.data == "image_autopost")
async def start_image_autopost(
    call: CallbackQuery, bot: Bot, state: FSMContext, user_id: int
):
    files = os.listdir("images")
    if "autopost.jpg" in files:
        await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        image = FSInputFile("images/autopost.jpg")
        new_msg = await bot.send_photo(
            chat_id=user_id,
            photo=image,
            caption="🌌 Autopost image is already set.\n\nPlease send the image you want to autopost.",
            reply_markup=await get_cancel_admin(),
        )
        await state.update_data({"msg_id": new_msg.message_id})

    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"🌌 Please send the image you want to autopost.",
            reply_markup=await get_cancel_admin(),
        )
        await state.update_data({"msg_id": call.message.message_id})

    await state.set_state(UploadImageAutopost.image)


@router.message(UploadImageAutopost.image, F.photo)
async def upload_image_autopost(
    message: Message, state: FSMContext, bot: Bot, user_id: int
):
    data = await state.get_data()
    msg_id = data["msg_id"]

    photo = message.photo[-1]  # самая большая версия
    file_id = photo.file_id

    try:
        os.remove("images/autopost.jpg")
    except:
        pass

    destination = f"images/autopost.jpg"
    await bot.download(file=file_id, destination=destination)

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await bot.delete_message(chat_id=user_id, message_id=data["msg_id"])

    await bot.send_message(
        chat_id=user_id,
        text=f"✅ Image uploaded successfully! File saved as {destination}.",
        reply_markup=await get_back_to_admin(),
    )
    await state.clear()
