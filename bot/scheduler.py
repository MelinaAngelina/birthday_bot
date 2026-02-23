import asyncio
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot

from .repository import BirthdayRepo
from .services import build_reminders
from .texts import format_reminder

TZ = ZoneInfo("Europe/Warsaw")

def _seconds_until_next_run(hour: int, minute: int) -> float:
    now = datetime.now(TZ)
    target = datetime.combine(now.date(), time(hour=hour, minute=minute), tzinfo=TZ)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()

async def reminder_loop(bot: Bot, repo: BirthdayRepo, days_before: int, hour: int, minute: int) -> None:
    while True:
        try:
            await asyncio.sleep(_seconds_until_next_run(hour, minute))
            today = datetime.now(TZ).date()

            user_ids = await repo.list_users()
            for uid in user_ids:
                rows = await repo.list_all(uid)
                items = build_reminders(rows, today=today, days_before=days_before)
                text = format_reminder(items)
                if text:
                    await bot.send_message(uid, text)
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(5)
