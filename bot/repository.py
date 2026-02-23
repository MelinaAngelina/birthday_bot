from dataclasses import dataclass
import aiosqlite
from typing import Optional, List

@dataclass(frozen=True)
class Birthday:
    user_id: int
    name: str
    day: int
    month: int
    year: Optional[int]

class BirthdayRepo:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def upsert_birthday(self, b: Birthday) -> None:
        sql = """
        INSERT INTO birthdays(user_id, name, day, month, year)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(user_id, name) DO UPDATE SET
            day=excluded.day, month=excluded.month, year=excluded.year
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql, (b.user_id, b.name, b.day, b.month, b.year))
            await db.commit()

    async def delete_by_name(self, user_id: int, name: str) -> int:
        sql = "DELETE FROM birthdays WHERE user_id=? AND name=?"
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(sql, (user_id, name))
            await db.commit()
            return cur.rowcount

    async def list_all(self, user_id: int) -> List[Birthday]:
        sql = """
        SELECT user_id, name, day, month, year
        FROM birthdays
        WHERE user_id=?
        ORDER BY month, day, name
        """
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(sql, (user_id,))
            rows = await cur.fetchall()
        return [Birthday(*row) for row in rows]

    async def list_users(self) -> List[int]:
        sql = "SELECT DISTINCT user_id FROM birthdays"
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(sql)
            rows = await cur.fetchall()
        return [r[0] for r in rows]
