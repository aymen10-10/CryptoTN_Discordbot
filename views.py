import discord
from discord.ext import commands
import os
import json
from views import MainMenuView

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

P2P_CHANNEL_ID = int(os.getenv("P2P_CHANNEL_ID"))
VENDEURS_CHANNEL_ID = int(os.getenv("VENDEURS_CHANNEL_ID"))
ACHETEURS_CHANNEL_ID = int(os.getenv("ACHETEURS_CHANNEL_ID"))

DB_PATH = "database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return {"vendeurs": [], "acheteurs": [], "transactions": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        await channel.purge()
        await channel.send(
            "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition ou publiez une offre :",
            view=MainMenuView(bot)
        )

bot.run(os.getenv("DISCORD_TOKEN"))
