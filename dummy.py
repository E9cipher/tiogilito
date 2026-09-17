# Dummy bot
import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot import canIReachDiscord

load_dotenv()  # read the token from .env

intents = discord.Intents.default()
intents.message_content = True
prefix = "!dy "


class GeneralDummyBot(commands.Cog):
    """General dummy bot commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(help="Check if the dummy bot is alive")
    async def ding(self, ctx: commands.Context["DummyBot"]) -> None:
        await ctx.send("dong")


class DummyBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.add_cog(GeneralDummyBot(self))


bot = DummyBot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    # Fires once the bot is connected
    user = bot.user
    print(f"Logged in as {user} (ID: {user.id if user is not None else 'NULL'})")
    print("Ready for duty")


async def startDummyBot():
    async with bot:
        env = os.getenv("DISCORD_DUMMY_TOKEN")
        if env is None:
            return discord.LoginFailure
        await bot.start(env)


try:
    asyncio.run(startDummyBot())
except KeyboardInterrupt:
    print("\nCtrl+C detected, exiting cleanly...")
except discord.LoginFailure:
    print("Discord login failure:")
    reachable = asyncio.run(canIReachDiscord())
    if reachable is False:
        print("Error: cannot connect to discord servers")
    if os.path.isfile(".env"):
        print(".env file found. Did the token expire?")
    else:
        print(".env file does not exist. Aaaand...")
        for _ in range(20):
            print("You didn't say the magic word!!!")
except Exception as e:  # noqa: BLE001
    print(f"Something went terribly wrong: {e}")
finally:
    print("\nSee ya!")
