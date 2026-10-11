import asyncio
import sqlite3

import aiosqlite


async def init_db():
    async with aiosqlite.connect("settings.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                should_ping BOOLEAN NOT NULL DEFAULT 1
            )
        """)
        await db.commit()


def check_db() -> bool:
    db = sqlite3.connect("settings.db")
    allok = True
    try:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        print("Integrity:", integrity)
        if integrity != "ok":
            allok = False

        tables = {
            row[0]
            for row in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        print("Has user_settings table:", "user_settings" in tables)
        if "user_settings" not in tables:
            allok = False

        if "user_settings" in tables:
            columns = {row[1] for row in db.execute("PRAGMA table_info(user_settings)")}
            expected = {"user_id", "should_ping"}
            print("Has expected columns:", expected <= columns)
            if not (expected <= columns):
                allok = False

            # Also confirm the query used by the bot works.
            db.execute("SELECT should_ping FROM user_settings WHERE user_id = ?", (1,))
            print("Bot query: OK")
    finally:
        db.close()

    return allok


async def get_shouldping(user_id: int) -> bool:
    if not check_db():
        raise ValueError("Invalid settings.db")
    async with aiosqlite.connect("settings.db") as db:
        cursor = await db.execute(
            "SELECT should_ping FROM user_settings WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        # If the user has no row yet, default to True (should_ping)
        return bool(row[0]) if row else True


async def set_shouldping(user_id: int, should_ping: bool):
    if not check_db():
        raise ValueError("Invalid settings.db")
    async with aiosqlite.connect("settings.db") as db:
        await db.execute(
            """
            INSERT INTO user_settings (user_id, should_ping)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET should_ping = excluded.should_ping
        """,
            (user_id, int(should_ping)),
        )
        await db.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
