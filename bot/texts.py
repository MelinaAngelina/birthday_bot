HELP_TEXT = (
    "Я помогу хранить дни рождения и напоминать за 3 дня.\n\n"
    "Команды:\n"
    "/add <имя> <дата> — добавить/обновить (DD.MM.YYYY или DD.MM)\n"
    "  пример: /add Катя 05.03.1999\n"
    "  пример: /add Паша 05.03\n"
    "/del <имя> — удалить\n"
    "  пример: /del Катя\n"
    "/list — показать список\n"
    "/help — помощь\n"
)

def format_list(rows) -> str:
    if not rows:
        return "Список пуст. Добавь запись командой: /add Имя 05.03.1999"
    lines = ["Твои дни рождения:"]
    for b in rows:
        if b.year:
            lines.append(f"• {b.name} — {b.day:02d}.{b.month:02d}.{b.year}")
        else:
            lines.append(f"• {b.name} — {b.day:02d}.{b.month:02d}")
    return "\n".join(lines)

def format_reminder(items) -> str:
    if not items:
        return ""
    lines = ["🎉 Скоро день рождения:"]
    for it in items:
        lines.append(f"• {it.name} — {it.event_date.strftime('%d.%m.%Y')} (через {it.days_left} дня)")
    return "\n".join(lines)
