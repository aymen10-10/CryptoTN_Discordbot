import discord
from discord.ext import commands
from discord.ui import View
from dotenv import load_dotenv
import os

from handlers import ButtonHandlerView

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs à définir dans les variables Railway
P2P_CHANNEL_ID = int(os.getenv("P2P_CHANNEL_ID"))
VENDEURS_CHANNEL_ID = int(os.getenv("VENDEURS_CHANNEL_ID"))
ACHETEURS_CHANNEL_ID = int(os.getenv("ACHETEURS_CHANNEL_ID"))

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

    # Envoie le menu dans le salon #p2p
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        await channel.purge(limit=100)
        await channel.send(
            "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une action ci-dessous :",
            view=ButtonHandlerView()
        )

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
