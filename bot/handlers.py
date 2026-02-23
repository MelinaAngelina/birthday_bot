from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from .repository import BirthdayRepo, Birthday
from .services import normalize_name, parse_date, ValidationError
from .texts import HELP_TEXT, format_list

router = Router()

def _split_args(args: str) -> tuple[str, str]:
    parts = (args or "").strip().split()
    if len(parts) < 2:
        raise ValidationError("Нужно указать имя и дату. Пример: /add Катя 05.03.1999")
    return parts[0], parts[1]

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer("Привет! " + HELP_TEXT)

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(HELP_TEXT)

@router.message(Command("add"))
async def cmd_add(msg: Message, command: CommandObject, repo: BirthdayRepo):
    try:
        name_raw, date_raw = _split_args(command.args or "")
        name = normalize_name(name_raw)
        d, mo, y = parse_date(date_raw)

        b = Birthday(user_id=msg.from_user.id, name=name, day=d, month=mo, year=y)
        await repo.upsert_birthday(b)
        suffix = f"{d:02d}.{mo:02d}.{y}" if y else f"{d:02d}.{mo:02d}"
        await msg.answer(f"✅ Сохранено: {name} — {suffix}")
    except ValidationError as e:
        await msg.answer(f"❌ {e}\n\n{HELP_TEXT}")
    except Exception:
        await msg.answer("⚠️ Что-то пошло не так. Попробуй ещё раз позже.")

@router.message(Command("del"))
async def cmd_del(msg: Message, command: CommandObject, repo: BirthdayRepo):
    try:
        name = normalize_name((command.args or "").strip())
        deleted = await repo.delete_by_name(msg.from_user.id, name)
        if deleted:
            await msg.answer(f"🗑️ Удалено: {name}")
        else:
            await msg.answer(f"Не нашла запись для имени: {name}")
    except ValidationError as e:
        await msg.answer(f"❌ {e}\n\nПример: /del Катя")
    except Exception:
        await msg.answer("⚠️ Ошибка при удалении. Попробуй ещё раз позже.")

@router.message(Command("list"))
async def cmd_list(msg: Message, repo: BirthdayRepo):
    try:
        rows = await repo.list_all(msg.from_user.id)
        await msg.answer(format_list(rows))
    except Exception:
        await msg.answer("⚠️ Не удалось получить список. Попробуй позже.")
