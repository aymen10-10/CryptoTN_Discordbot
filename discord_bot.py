import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté avec succès.")

@bot.command()
async def test(ctx):
    await ctx.send("Le bot Discord fonctionne !")

# Chargement du token depuis Railway (variable d'environnement)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("ERREUR : le token est vide ou introuvable.")
else:
    bot.run(TOKEN)
