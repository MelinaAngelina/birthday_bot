import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import load_config
from .db import init_db
from .repository import BirthdayRepo
from .handlers import router
from .scheduler import reminder_loop

async def main():
    logging.basicConfig(level=logging.INFO)

    cfg = load_config()
    await init_db(cfg.db_path)

    bot = Bot(token=cfg.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    repo = BirthdayRepo(cfg.db_path)

    dp.include_router(router)

    reminder_task = asyncio.create_task(
        reminder_loop(bot, repo, cfg.remind_days_before, cfg.remind_hour, cfg.remind_minute)
    )

    try:
        await dp.start_polling(bot, repo=repo)
    finally:
        reminder_task.cancel()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
