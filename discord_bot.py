import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class RoleSelectionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleButton("Acheteur", "buyer"))
        self.add_item(RoleButton("Vendeur", "seller"))

class RoleButton(Button):
    def __init__(self, label, role):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=f"role_{role}")
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Vous avez choisi le rôle **{self.role}**. Veuillez sélectionner un utilisateur pour démarrer.",
            ephemeral=True,
            view=UserSelectionView(self.role)
        )

class UserSelectionView(View):
    def __init__(self, role):
        super().__init__(timeout=1200)  # 20 minutes
        self.role = role
        self.add_item(UserInputModal(role))

class UserInputModal(Button):
    def __init__(self, role):
        super().__init__(label="Saisir le montant", style=discord.ButtonStyle.success, custom_id=f"modal_{role}")
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        modal = TransactionModal(self.role)
        await interaction.response.send_modal(modal)

class TransactionModal(Modal, title="Détails de la transaction"):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.amount = TextInput(label="Montant en USDT", placeholder="Ex: 100", required=True)
        self.add_item(self.amount)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Transaction lancée par **{interaction.user}** en tant que **{self.role}** pour {self.amount.value} USDT.",
            ephemeral=False
        )

@bot.command(name="start")
async def start(ctx):
    await ctx.send("Choisissez votre rôle :", view=RoleSelectionView())

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
