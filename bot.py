from discord.ext import commands
from dotenv import load_dotenv
import discord
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
    embed = discord.Embed(title = message, description="Bullish Trend", color=discord.Color.green())
    embed.set_author(name="Indicator", icon_url="https://i.imgur.com/cgEEz1h.png")
    embed.set_thumbnail(url="https://i.imgur.com/sn0HQ84.png")
    embed.url = ("https://www.binance.com/en/trade/BTC_USDT?theme=dark&type=spot")
    await channel.send(embed=embed)

async def trade_identifier(result, symbol):
    if result == "Decrease":
        message = symbol + ": Decreasing bullish trade identified."
    elif result == "Increase":
        message = symbol + ": Increasing bullish trade identified"
    else:
        message = symbol + ": No trade identified."

    await send_discord_notification(message)

async def start_bot():
    await bot.start(bot_token)