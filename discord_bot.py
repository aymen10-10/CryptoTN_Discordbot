import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== Boutons interactifs ======
class DispositionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DispositionButton("USDT (TRC20)"))
        self.add_item(DispositionButton("RedotPay"))
        self.add_item(DispositionButton("Neteller"))
        self.add_item(DispositionButton("Skrill"))

class DispositionButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Voici les offres disponibles pour **{self.label}** (prochainement dynamiques).", ephemeral=True
        )

# ====== Quand le bot démarre ======
@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne.")
    channel = discord.utils.get(bot.get_all_channels(), name="p2p")

    if channel:
        # Supprimer anciens messages du bot pour éviter les doublons
        async for msg in channel.history(limit=10):
            if msg.author == bot.user:
                await msg.delete()

        # Envoyer le menu automatique
        await channel.send(
            "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition de vente ci-dessous :",
            view=DispositionView()
        )

# ====== Démarrage du bot ======
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
