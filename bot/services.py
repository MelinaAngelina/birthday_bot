from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple, List
import re

from .repository import Birthday

DATE_RE_FULL = re.compile(r"^(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})$")
DATE_RE_SHORT = re.compile(r"^(\d{1,2})[.\-/](\d{1,2})$")

class ValidationError(ValueError):
    pass

def normalize_name(raw: str) -> str:
    name = (raw or "").strip()
    if not name:
        raise ValidationError("Имя не должно быть пустым.")
    if len(name) > 64:
        raise ValidationError("Имя слишком длинное (макс. 64 символа).")
    return name

def parse_date(raw: str) -> Tuple[int, int, Optional[int]]:
    s = (raw or "").strip()
    if not s:
        raise ValidationError("Дата не должна быть пустой.")

    m = DATE_RE_FULL.match(s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        _validate_calendar(d, mo, y)
        return d, mo, y

    m = DATE_RE_SHORT.match(s)
    if m:
        d, mo = int(m.group(1)), int(m.group(2))
        _validate_calendar(d, mo, 2000)
        return d, mo, None

    raise ValidationError("Неверный формат даты. Используй DD.MM.YYYY или DD.MM (например 05.03.1999 или 05.03).")

def _validate_calendar(d: int, mo: int, y: int) -> None:
    try:
        date(y, mo, d)
    except ValueError:
        raise ValidationError("Такой даты не существует. Проверь день/месяц/год.")

def next_occurrence(day: int, month: int, today: date) -> date:
    year = today.year
    try_date = date(year, month, day)
    if try_date < today:
        try_date = date(year + 1, month, day)
    return try_date

@dataclass(frozen=True)
class ReminderItem:
    name: str
    event_date: date
    days_left: int

def build_reminders(birthdays: List[Birthday], today: date, days_before: int) -> List[ReminderItem]:
    items: List[ReminderItem] = []
    for b in birthdays:
        occ = next_occurrence(b.day, b.month, today)
        delta = (occ - today).days
        if delta == days_before:
            items.append(ReminderItem(name=b.name, event_date=occ, days_left=delta))
    items.sort(key=lambda x: (x.event_date, x.name.lower()))
    return items
