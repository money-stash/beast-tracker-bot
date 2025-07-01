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
                callback_data="open_partner_manager",
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
                text="🎯 Mini-Challenge Control Center",
                callback_data="open_challenges_control",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏋️‍♀️ Daily Motivation Broadcast",
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
                callback_data=f"user_full_history_{user_id}",
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


async def get_admin_settings_menu():
    kb = [
        [
            InlineKeyboardButton(
                text="⏰ Set DME check-in hours", callback_data="set_dme_hours"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚀 Define streak milestone triggers",
                callback_data="strak_triggers",
            )
        ],
        [
            InlineKeyboardButton(
                text="♻️ Configure partner rotation frequency",
                callback_data="change_partnet_rotation",
            )
        ],
        [
            InlineKeyboardButton(
                text="📤 Upload branded images/graphics for auto-posts",
                callback_data="image_autopost",
            )
        ],
        [
            InlineKeyboardButton(
                text="🗓️ Adjust Wall of Fame posting date/time",
                callback_data="asdasdasd",
            )
        ],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_daily_motivation_menu():
    kb = [
        [InlineKeyboardButton(text="🧭 Schedule", callback_data="schedule_message")],
        [
            InlineKeyboardButton(
                text="🕰️ Scheduled messages", callback_data="scheduled_messages"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Send manual messages", callback_data="send_manual_msg"
            )
        ],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_message_center_menu():
    kb = [
        [InlineKeyboardButton(text="✉️ Send DM", callback_data="send_dm")],
        [
            InlineKeyboardButton(
                text="📢 Broadcast to specific segments", callback_data="asdasd"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗂️ Template manager ", callback_data="template_manager"
            )
        ],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_partner_menager():
    kb = [
        [
            InlineKeyboardButton(
                text="Current pairing view", callback_data="current_partners"
            )
        ],
        [
            InlineKeyboardButton(
                text="Re-pair individuals or full-group reassign",
                callback_data="reload_partners",
            )
        ],
        [
            InlineKeyboardButton(
                text="Trigger 1-on-1 check-ins between partners",
                callback_data="partners_versus",
            )
        ],
        [
            InlineKeyboardButton(
                text="See partner nudges sent / received",
                callback_data="partners_nudges",
            )
        ],
        [
            InlineKeyboardButton(
                text="Set next auto-rotation date",
                callback_data="set_partners_auto_rotation",
            )
        ],
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def get_challenges_menu(challenges):
    kb = []

    for challenge in challenges:
        kb.append(
            [
                InlineKeyboardButton(
                    text=challenge.name,
                    callback_data=f"open_admin_challenge_{challenge.id}",
                )
            ]
        )

    kb.append(
        [
            InlineKeyboardButton(
                text="➕ Add new challenge", callback_data="add_new_challenge"
            )
        ],
    )
    kb.append(
        [InlineKeyboardButton(text="🔙 Admin menu", callback_data="back_to_admin")],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
