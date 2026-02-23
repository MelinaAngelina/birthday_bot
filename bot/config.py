import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    db_path: str = "birthdays.sqlite3"
    remind_days_before: int = 3
    remind_hour: int = 9
    remind_minute: int = 0

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in environment (.env).")
    return Config(bot_token=token)
