from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_admin_menu():
    kb = [
        [InlineKeyboardButton(text="📊 Dashboard", callback_data="open_dashboard")],
        [
            InlineKeyboardButton(
                text="🏘️ Member Directory", callback_data="open_mem_directory"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Group settings", callback_data="open_group_settings"
            )
        ],
        [InlineKeyboardButton(text="🔙 Main menu", callback_data="back_to_main")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_group_settings_menu():
    kb = [
        [InlineKeyboardButton(text="🔄 Change group", callback_data="change_group")],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_back_to_admin():
    kb = [
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
