import os
import aiosqlite
from discord.ext import commands
import asyncio

DB_PATH = "cogs/Tickets/ticket.db"

async def setup_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ticket_config (
                guild_id         INTEGER PRIMARY KEY,
                panel_channel_id INTEGER,
                category_id      INTEGER,
                embed_message_id INTEGER,
                staff_role_id    INTEGER,
                ticket_count     INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def set_ticket_config(guild_id, panel_channel_id, category_id, embed_message_id, staff_role_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO ticket_config (
                guild_id, panel_channel_id, category_id, embed_message_id, staff_role_id
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                panel_channel_id = excluded.panel_channel_id,
                category_id      = excluded.category_id,
                embed_message_id = excluded.embed_message_id,
                staff_role_id    = excluded.staff_role_id
        """, (guild_id, panel_channel_id, category_id, embed_message_id, staff_role_id))
        await db.commit()


async def get_ticket_config(guild_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM ticket_config WHERE guild_id = ?", (guild_id,)
        ) as cursor:
            return await cursor.fetchone()


async def increment_ticket_count(guild_id) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE ticket_config
            SET ticket_count = ticket_count + 1
            WHERE guild_id = ?
        """, (guild_id,))
        await db.commit()

        async with db.execute(
            "SELECT ticket_count FROM ticket_config WHERE guild_id = ?", (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]


async def delete_ticket_config(guild_id) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM ticket_config WHERE guild_id = ?", (guild_id,)
        )
        await db.commit()
        return cursor.rowcount > 0

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.run(setup_tables())

def setup(bot):
    bot.add_cog(Database(bot))

