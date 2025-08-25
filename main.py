import asyncio
from apscheduler.triggers.cron import CronTrigger

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties


from handlers.user import user_commands
from callbacks.user import (
    open_profile,
    back_to_main,
    daily_ok,
    open_daily_tasks,
    add_daily_task,
    delete_daily_task,
    set_done_daily,
    user_challenges,
    open_user_challenge,
    exec_challenge,
    open_daily_statistic,
    notify_group_done,
    open_challenge_stats,
)
from callbacks.admin import (
    open_admin,
    open_group_settings,
    change_group,
    open_dashboard,
    cancel_admin,
    open_mem_directory,
    ban_user,
    open_settings,
    open_daily_motivation,
    open_messages_center,
    open_partner_manager,
    change_partnet_rotation,
    send_dm,
    open_challenges_control,
    add_challenge,
    open_admin_challenge,
    delete_challenge,
    schedule_message,
    open_scheduled_messages,
    schedule_msg_info,
    delete_scheduled,
    user_full_history,
    manually_adjust_streak,
    open_leaderboard,
    current_partners,
    open_check_menagement,
    open_export,
    set_dme,
    image_autopost,
    next_rotation_date,
    mngmnt_data,
    open_admin_permission,
    open_perm,
    set_perm,
)

from middlewares.user_info import UserInfoMiddleware
from utils.remainders import shchedule_daily_remainders, schedule_daily_db_backup

from database.db import db
from config import TOKEN, us_tz, scheduler


async def scheduled_task(bot: Bot):
    print("scheduled_task successffully executed")
    await db.cleanup_daily_tasks()


async def challenge_checker(bot: Bot):
    print("challenge_checker successfully executed")
    challenges = await db.get_all_challenges()
    for challenge in challenges:
        if await db.is_challenge_expired(challenge.id):
            print(f"Challenge {challenge.id} is expired")

            users = await db.get_users()
            for user in users:
                try:
                    stats_text = await db.get_mini_challenge_stats(
                        user.user_id, challenge.id
                    )
                    await bot.send_message(
                        user.user_id,
                        f"Challenge {challenge.id} is expired.\n\nYour stats:\n{stats_text}",
                    )
                except Exception as e:
                    pass

            await db.delete_challenge(challenge.id)

        else:
            print(f"Challenge {challenge.id} is still active")


async def main():
    await db.init_models()

    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.outer_middleware(UserInfoMiddleware())
    dp.callback_query.outer_middleware(UserInfoMiddleware())

    dp.include_routers(
        user_commands.router,
        open_profile.router,
        back_to_main.router,
        daily_ok.router,
        open_daily_tasks.router,
        add_daily_task.router,
        delete_daily_task.router,
        set_done_daily.router,
        open_admin.router,
        open_group_settings.router,
        change_group.router,
        open_dashboard.router,
        cancel_admin.router,
        open_mem_directory.router,
        ban_user.router,
        open_settings.router,
        open_daily_motivation.router,
        open_messages_center.router,
        open_partner_manager.router,
        change_partnet_rotation.router,
        send_dm.router,
        open_challenges_control.router,
        add_challenge.router,
        open_admin_challenge.router,
        delete_challenge.router,
        user_challenges.router,
        open_user_challenge.router,
        exec_challenge.router,
        schedule_message.router,
        open_scheduled_messages.router,
        schedule_msg_info.router,
        delete_scheduled.router,
        user_full_history.router,
        manually_adjust_streak.router,
        open_leaderboard.router,
        current_partners.router,
        open_check_menagement.router,
        open_export.router,
        set_dme.router,
        image_autopost.router,
        next_rotation_date.router,
        mngmnt_data.router,
        open_daily_statistic.router,
        open_admin_permission.router,
        open_perm.router,
        set_perm.router,
        notify_group_done.router,
        open_challenge_stats.router,
    )

    scheduler.add_job(
        scheduled_task, CronTrigger(hour=2, minute=0, timezone=us_tz), args=[bot]
    )
    scheduler.add_job(
        challenge_checker, CronTrigger(hour=2, minute=0, timezone=us_tz), args=[bot]
    )
    scheduler.add_job(
        db.back_daily_to_history, CronTrigger(hour=2, minute=0, timezone=us_tz)
    )
    # await db.back_daily_to_history()
    scheduler.add_job(
        db.check_all_challenges_today, CronTrigger(hour=2, minute=0, timezone=us_tz)
    )
    # await db.check_all_challenges_today()

    # notifier
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=7, minute=0, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=10, minute=30, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=13, minute=55, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=17, minute=40, timezone=us_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=19, minute=25, timezone=us_tz),
        args=[bot],
    )

    # backup
    scheduler.add_job(
        schedule_daily_db_backup,
        CronTrigger(hour=12, minute=00, timezone=us_tz),
        args=[bot],
    )

    scheduler.start()

    await db.assign_random_partners()
    await db.update_leaderboard()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
