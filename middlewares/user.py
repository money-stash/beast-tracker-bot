from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_main_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    kb_btns = [
        [
            InlineKeyboardButton(text="‼️ Daily", callback_data="daily_tasks"),
            InlineKeyboardButton(text="🎯 Challenges", callback_data="user_challenges"),
        ],
        [
            InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
        ],
    ]
    # InlineKeyboardButton(text="🔔 Remainders", callback_data="my_remainders"),
    if is_admin:
        kb_btns.append(
            [InlineKeyboardButton(text="👩‍💼 Admin panel", callback_data="open_admin")]
        )

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


async def get_challenges_menu(challenges):
    kb = []

    for challenge in challenges:
        kb.append(
            [
                InlineKeyboardButton(
                    text=challenge.name,
                    callback_data=f"open_user_challenge_{challenge.id}",
                )
            ]
        )

    kb.append(
        [InlineKeyboardButton(text="🔙 Main menu", callback_data="back_to_main")],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
