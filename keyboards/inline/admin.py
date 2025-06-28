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
        [
            InlineKeyboardButton(
                text="👥 Accountability Partner Manager",
                callback_data="open_partner_menager",
            )
        ],
        [
            InlineKeyboardButton(
                text="Check-In Management",
                callback_data="open_check_menagement",
            )
        ],
        [
            InlineKeyboardButton(
                text="🥇 Leaderboards & Achievements",
                callback_data="open_leaderboard",
            )
        ],
        [
            InlineKeyboardButton(
                text="Mini-Challenge Control Center",
                callback_data="open_challenges_control",
            )
        ],
        [
            InlineKeyboardButton(
                text="Daily Motivation Broadcast",
                callback_data="open_motivation",
            )
        ],
        [
            InlineKeyboardButton(
                text="📫 Messaging Center",
                callback_data="open_messages_center",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Settings & Customization",
                callback_data="open_settings",
            )
        ],
        [
            InlineKeyboardButton(
                text="🖨️ Export & Reports",
                callback_data="open_export",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔑 Admin Roles & Permissions",
                callback_data="open_admin_permission",
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


async def get_cancel_admin():
    kb = [
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_mem_user_menu(user_id: int):
    kb = [
        [
            InlineKeyboardButton(
                text="📊 View full history",
                callback_data=f"user_full_histiry_{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚜️ Manually adjust streak",
                callback_data=f"manually_adjust_streak_{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="✉️ Send manual message",
                callback_data=f"send_manual_message_{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑️ Remove from group", callback_data=f"ban_user_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Assign accountability partner manually",
                callback_data=f"add_parthner_{user_id}",
            )
        ],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
