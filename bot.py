import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from db_setup import get_shouldping, set_shouldping

load_dotenv()  # read the token from .env

# Intents controls the data Discord sends to the bot
# message_content is required to read message text in commands
intents = discord.Intents.default()
intents.message_content = True
prefix = "!dn "

# ctx the message object
# ctx.send -> reply on the same channel
# ctx.message.reply -> reply to the message (on ctx)
roles = {"Moderator": 1534940065912848424, "normal dude": 1534940714280943767}


class General(commands.Cog):
    """General bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Check if the bot is alive")
    async def ping(self, ctx):
        await sendMessage(ctx, "pong")

    @commands.command(help="Say hello to a new member (or yourself)")
    async def sayhi(
        self,
        ctx,
        member: discord.Member = commands.parameter(
            default=None,
            displayed_default="yourself",
            description="The member to greet",
        ),
    ):
        if bot.user in ctx.message.mentions:
            return
        if member is None:
            member = ctx.author
        announcements = getChannel("announcements")
        announce_mention = (
            announcements.mention if announcements is not None else "#announcements"
        )
        await sendMessage(
            ctx,
            f"Hello {member.mention}, welcome! Make sure to read {announce_mention}!",
        )

    @commands.command(help="YouTube link to a very useful tutorial")
    async def tutorial(self, ctx):
        await sendMessage(ctx, "<https://www.youtube.com/watch?v=dQw4w9WgXcQ>")


class Fun(commands.Cog):
    """Funny commands, very useful"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mickey(self, ctx):
        await sendMessage(ctx, "mouse 🐭")


class Settings(commands.Cog):
    """To adjust preferences"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Whether the bot should reply to your messages or not")
    async def shouldping(
        self,
        ctx,
        value: str | None = commands.parameter(
            description="on/off, leave empty for status",
        ),
    ):
        current = await get_shouldping(ctx.author.id)
        if value is None or value == "status":
            await sendMessage(
                ctx, f"You have replies turned {'On' if current else 'Off'}"
            )
            return
        if value == "on":
            if current is True:
                await sendMessage(ctx, "Hmmmm, replies are already on!")
                return
            await set_shouldping(ctx.author.id, True)
            await sendMessage(ctx, "Replies turned On")
        elif value == "off":
            if current is False:
                await sendMessage(ctx, "Hmmmm, replies are already off!")
                return
            await set_shouldping(ctx.author.id, False)
            await sendMessage(ctx, "Replies are turned Off")
        else:
            await sendMessage(
                ctx,
                f"Warning: invalid value {value}. Use `on` or `off` and learn to write!",
            )


class Moderation(commands.Cog):
    """Moderator-only actions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Ban a specific user")
    @commands.has_role(roles["Moderator"])
    async def ban(
        self,
        ctx,
        user: discord.member = commands.parameter(description="The member to ban"),
    ):
        await user.ban()
        await sendMessage(ctx, f"User {user} has been successfully banned")


class TioGilitoBot(commands.Bot):
    async def setup_hook(self):
        # add_cog registers all commands inside that cog with the bot
        await self.add_cog(General(self))
        await self.add_cog(Fun(self))
        await self.add_cog(Settings(self))
        await self.add_cog(Moderation(self))


bot = TioGilitoBot(command_prefix=prefix, intents=intents)
channels = {
    "general": 1534937452026921012,
    "announcements": 1534947035185156276,
    "spam": 1534939255799943411,
}


def getChannel(channel: str):
    # Return the channel object or None if not found
    if channel not in channels:
        return None
    return bot.get_channel(channels[channel])


def isModerator(user: discord.Member):
    return any(role.id == roles["Moderator"] for role in user.roles)


@bot.event
async def on_ready():
    # Fires once the bot is connected
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Ready for duty")


@bot.event
async def on_message(message):
    # Ignore the bot's own messages, to avoid infinite loops
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        await message.add_reaction("👋")
        await message.reply(f"Hey {message.author.mention}, that's me!")

    # IMPORTANT: still check for commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    # Send a friendly message when I don't know what the hell they sent
    if isinstance(error, commands.CommandNotFound):
        invoked = (
            ctx.message.content.split()[1]
            if getattr(ctx.message, "content", None)
            else "that command"
        )
        await sendMessage(
            ctx,
            f'Ummm where did you learn to write? "{invoked}" is not a valid command. Learn to use {prefix}help to list commands.',
        )
    elif isinstance(error, commands.MissingRole):
        await sendMessage(
            ctx, f"Nice try, but you need the `{error.missing_role}` role for that"
        )
    else:
        # Log other errors for debugging
        print(f"Unhandled command error: {error}")


async def sendMessage(ctx, message: str):
    reply = await get_shouldping(ctx.author.id)
    newMessage = message + "\n"
    newMessage += "-# 🪙🪙💸 - @e9cipher if I misbehave"
    if reply:
        await ctx.reply(newMessage)
    else:
        await ctx.send(newMessage)


async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Ctrl+C detected, exiting cleanly...")
except discord.LoginFailure:
    print("Discord login failure:")
    if os.path.isfile(".env"):
        print(".env file found. Did the token expire?")
    else:
        print(".env file does not exist. Aaaand...")
        for x in range(20):
            print("You didn't say the magic word!!!")
except Exception as e:  # noqa: BLE001
    print(f"Something went terribly wrong: {e}")
finally:
    print("\nSee ya!")
