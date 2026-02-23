# Birthday Reminder Telegram Bot (Python / aiogram 3)

Бот хранит дни рождения друзей отдельно для каждого пользователя и присылает напоминание **за 3 дня** до события.

## Возможности
- `/add <имя> <дата>` — добавить/обновить (формат `DD.MM.YYYY` или `DD.MM`)
- `/del <имя>` — удалить
- `/list` — показать список
- `/help` — подсказка

Данные хранятся в SQLite (файл `birthdays.sqlite3` создаётся автоматически).

Напоминания отправляются ежедневно в **09:00 Europe/Warsaw** (настраивается в `bot/config.py`).

## Установка и запуск

1) Создайте бота в BotFather и получи токен.

2) В корне проекта создайте файл `.env`:
```env
BOT_TOKEN=123456:ABCDEF....
```

3) Установи зависимости и запусти:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m bot.main
```

## Примеры
- Добавить: `/add Катя 05.03.1999`
- Добавить без года: `/add Паша 05.03`
- Удалить: `/del Катя`
- Список: `/list`

## Архитектура
- `bot/handlers.py` — обработчики команд
- `bot/repository.py` — слой доступа к данным (SQLite)
- `bot/services.py` — валидация и бизнес-логика (расчёт напоминаний)
- `bot/scheduler.py` — ежедневная фоновая проверка и рассылка
- `bot/db.py` — инициализация схемы БД

тест пуш