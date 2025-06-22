from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_main_menu() -> InlineKeyboardMarkup:
    kb_btns = [
        [InlineKeyboardButton(text="‼️ Daily", callback_data="daily_tasks")],
        [InlineKeyboardButton(text="⚖️ Weekly", callback_data="weekly_tasks")],
        [InlineKeyboardButton(text="🔔 Remainders", callback_data="my_remainders")],
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb


async def get_back_to_main_menu() -> InlineKeyboardMarkup:
    kb_btns = [
        [InlineKeyboardButton(text="🔙 Main menu", callback_data="back_to_main")],
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb


async def get_back_to_daily_menu() -> InlineKeyboardMarkup:
    kb_btns = [
        [InlineKeyboardButton(text="🔙 Daily", callback_data="back_to_daily")],
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb


async def get_daily_menu() -> InlineKeyboardMarkup:
    kb_btns = [
        [
            InlineKeyboardButton(text="➕ Add", callback_data="add_daily_task"),
            InlineKeyboardButton(text="➖ Delete", callback_data="remove_daily_task"),
        ],
        [
            InlineKeyboardButton(
                text="✅ Mark completed", callback_data="done_daily_task"
            ),
        ],
        [InlineKeyboardButton(text="📊 Statistic", callback_data="daily_statistic")],
        [InlineKeyboardButton(text="🔙 Main menu", callback_data="back_to_main")],
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb


async def get_accept_cancel_keyboard() -> InlineKeyboardMarkup:
    kb_btns = [
        [
            InlineKeyboardButton(text="✅ Yes", callback_data="accept"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel"),
        ]
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb


async def get_daily_ok() -> InlineKeyboardMarkup:
    kb_btns = [
        [
            InlineKeyboardButton(text="💪 I'll do my best!", callback_data="ok_daily"),
        ]
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_btns, resize_keyboard=True)
    return kb
