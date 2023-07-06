from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user.name}")

async def send_discord_notification(message):
    channel_id = 1125539153803751465
    channel = bot.get_channel(channel_id)
    await channel.send(message)

async def trade_identifier(result):
    if result == "Decrease":
        message = "Decreasing bullish trade identified."
    elif result == "Increase":
        message = "Increasing bullish trade identified"
    else:
        message = "No trade identified."

    await send_discord_notification(message)

async def start_bot():
    await bot.start(bot_token)