import os
from datetime import datetime, timezone
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() # read the token from .env

# Intents control the data Discord sends to the bot.
# message_content is required to read message text in commands
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
channels = {
    "general": 1534937452026921012,
    "announcements": 1534947035185156276,
    "spam": 1534939255799943411,
    "juegos": 1534950293605843005
}

def getChannel(channel: str):
    # Return the channel object or None if not found
    if channel not in channels:
        return None
    return bot.get_channel(channels[channel])

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
        await message.reply(f"Yoooo {message.author.mention} that's me!")
        await message.add_reaction("👋")

    # IMPORTANT: still check for commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    # Send a friendly message when I don't know what the hell they sent
    if isinstance(error, commands.CommandNotFound):
        invoked = ctx.message.content.split()[0] if getattr(ctx.message, 'content', None) else 'that command'
        await sendMessage(ctx, f"Unknown command: {invoked}. Use !help to list commands.", True)
    else:
        # Log other errors for debugging
        print(f"Unhandled command error: {error}")

async def sendMessage(ctx, message: str, reply: bool = False):
    newMessage = message + "\n"
    newMessage += f"-# \- {bot.user} at {datetime.now(timezone.utc).isoformat()}"
    if reply:
        await ctx.message.reply(newMessage)
    else:
        await ctx.send(newMessage)

# ctx the message object
# ctx.send -> reply on the same channel
# ctx.message.reply -> reply to the message (on ctx)

@bot.command()
async def ping(ctx):
    await sendMessage(ctx, "pong")

@bot.command()
async def sayhi(ctx, member: discord.Member = None):
    if (member is None): member = ctx.author
    announcements = getChannel('announcements')
    announce_mention = announcements.mention if announcements is not None else '#announcements'
    await sendMessage(ctx, f"Hello {member.mention}, welcome! Make sure to read {announce_mention}!", True)

try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except KeyboardInterrupt:
    print("Ctrl+C detected, exiting cleanly...")
except discord.LoginFailure:
    print("Discord login failure. Check .env for the OAuth2 token. Did it expire?")
except Exception as e:
    print(f"Something went terribly wrong: {e}")
finally:
    print("\nSee ya!")