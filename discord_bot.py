import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

transactions = {}

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne !")

@bot.command()
async def test(ctx):
    await ctx.send("Le bot Discord fonctionne !")

from discord.ui import View, Button

class EscrowView(View):
    def __init__(self, montant, acheteur, vendeur):
        super().__init__(timeout=None)
        self.montant = montant
        self.acheteur = acheteur
        self.vendeur = vendeur
        self.status = "en attente"

    @discord.ui.button(label="Bloquer les fonds", style=discord.ButtonStyle.primary)
    async def lock_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.vendeur:
            await interaction.response.send_message("Seul le vendeur peut bloquer les fonds.", ephemeral=True)
            return
        self.status = "bloqué"
        await interaction.response.send_message(f"Fonds simulés comme bloqués ({self.montant} USDT). En attente de confirmation de l'acheteur...")

    @discord.ui.button(label="Confirmer la transaction", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.acheteur:
            await interaction.response.send_message("Seul l'acheteur peut confirmer la transaction.", ephemeral=True)
            return
        if self.status != "bloqué":
            await interaction.response.send_message("Les fonds ne sont pas encore bloqués.", ephemeral=True)
            return
        self.status = "confirmé"
        await interaction.response.send_message("Transaction confirmée. USDT libérés au vendeur !")

@bot.command()
async def escrow(ctx, montant: float, acheteur: discord.Member, vendeur: discord.Member):
    view = EscrowView(montant, acheteur, vendeur)
    await ctx.send(
        f"**Transaction interactive**\nMontant : `{montant} USDT`\nAcheteur : {acheteur.mention}\nVendeur : {vendeur.mention}",
        view=view
    )
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
