import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Select, Modal, TextInput
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Vue principale avec boutons Acheteur / Vendeur
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
        await interaction.response.send_message(f"Voici la liste des {self.label.lower()}s disponibles :", ephemeral=True, view=UserListView(self.role))

# Vue pour choisir un utilisateur et entrer le montant
class UserListView(View):
    def __init__(self, role):
        super().__init__(timeout=None)
        self.role = role
        self.add_item(UserSelect(role))

class UserSelect(Select):
    def __init__(self, role):
        options = [
            discord.SelectOption(label="Utilisateur 1", value="user1"),
            discord.SelectOption(label="Utilisateur 2", value="user2")
        ]
        super().__init__(placeholder="Choisissez un utilisateur", options=options, custom_id=f"select_{role}")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MontantModal(self.values[0]))

# Modal pour entrer le montant
class MontantModal(Modal):
    def __init__(self, selected_user):
        super().__init__(title="Entrer le montant", custom_id="modal_montant")
        self.selected_user = selected_user
        self.amount = TextInput(label="Montant en USDT", placeholder="Ex: 50", custom_id="amount_input")
        self.add_item(self.amount)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Transaction avec {self.selected_user} pour {self.amount.value} USDT. Une fenêtre temporaire est ouverte pour 20 minutes.", ephemeral=True)
        await asyncio.sleep(1200)
        await interaction.followup.send("Fenêtre expirée. La transaction a été annulée.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne !")

@bot.command()
async def start(ctx):
    await ctx.send("Choisissez votre rôle :", view=RoleSelectionView())

bot.run(os.getenv("TOKEN"))
