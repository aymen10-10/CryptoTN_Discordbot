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

P2P_CHANNEL_ID = int(os.getenv("P2P_CHANNEL_ID"))  # Assure-toi que cette variable est bien définie

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        await channel.purge(limit=10)
        await channel.send("Bienvenue sur le P2P CryptoTN !", view=MainMenuView())
    else:
        print("Salon introuvable.")

# Commande pour forcer le menu (utile en cas de reset)
@bot.command()
async def menu(ctx):
    await ctx.send("Menu principal :", view=MainMenuView())

bot.run(os.getenv("DISCORD_TOKEN"))
