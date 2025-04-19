import discord
import os
from discord.ext import commands
from views import MainMenuView
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
P2P_CHANNEL_ID = int(os.getenv("P2P_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        await channel.purge(limit=10)
        await channel.send("Bienvenue sur CryptoTN P2P ! Choisissez une option :", view=MainMenuView())

bot.run(TOKEN)
