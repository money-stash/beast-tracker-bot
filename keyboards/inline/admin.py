from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_admin_menu():
    kb = [
        [InlineKeyboardButton(text="📊 Dashboard", callback_data="open_dashboard")],
        [
            InlineKeyboardButton(
                text="🏘️ Member Directory", callback_data="open_mem_directory"
            )
        ],
        [InlineKeyboardButton(text="🔙 Main menu", callback_data="back_to_main")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
