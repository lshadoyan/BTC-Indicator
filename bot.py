import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user.name}")

async def send_discord_notification(message):
    channel_id = 1125539153803751465 

    channel = bot.get_channel(channel_id)
    await channel.send(message)

def trade_identifier(result):
    if result == "Decrease":
        message = "Decreasing bullish trade identified."
    elif result == "Increasing":
        message = "Increasing bullish trade identified"
    else:
        message = "No trade identified."

    bot.loop.create_task(send_discord_notification(message))

def start_bot():
    bot.run(bot_token)
