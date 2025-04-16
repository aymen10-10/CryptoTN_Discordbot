import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne !")

@bot.command()
async def test(ctx):
    await ctx.send("Le bot Discord fonctionne bien !")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
