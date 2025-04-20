import discord
from discord.ext import commands
import os
from views import MainMenuView
from utils import load_database, save_database

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    channel_id = int(os.getenv("P2P_CHANNEL_ID"))
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.purge(limit=10)
        await channel.send("**Bienvenue dans le système P2P. Choisissez une option :**", view=MainMenuView())

bot.run(os.getenv("DISCORD_TOKEN"))
