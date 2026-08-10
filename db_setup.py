import asyncio
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

async def get_shouldping(user_id: int) -> bool:
    async with aiosqlite.connect("settings.db") as db:
        cursor = await db.execute(
            "SELECT should_ping FROM user_settings WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        # If the user has no row yet, default to True (should_ping)
        return bool(row[0]) if row else True

async def set_shouldping(user_id: int, should_ping: bool):
    async with aiosqlite.connect("settings.db") as db:
        await db.execute("""
            INSERT INTO user_settings (user_id, should_ping)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET should_ping = excluded.should_ping
        """, (user_id, int(should_ping)))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
