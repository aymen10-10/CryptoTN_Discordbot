import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class TransactionModal(Modal):
    def __init__(self, role):
        super().__init__(title=f"{role} - Nouvelle transaction")
        self.role = role
        self.amount = TextInput(label="Montant (en USDT)", placeholder="Ex: 100", required=True)
        self.add_item(self.amount)

    async def on_submit(self, interaction: discord.Interaction):
        montant = self.amount.value
        await interaction.response.send_message(
            f"Transaction démarrée en tant que **{self.role}** pour **{montant} USDT**. Un salon sera créé bientôt.",
            ephemeral=True
        )

        # Créer un salon privé (facultatif : tu peux y ajouter logique de permissions)
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(
            name=f"{self.role.lower()}-{interaction.user.name}",
            overwrites=overwrites
        )
        await channel.send(f"Bienvenue {interaction.user.mention} ! La transaction de **{montant} USDT** démarre ici.")

class RoleSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Acheteur", style=discord.ButtonStyle.success, custom_id="buy"))
        self.add_item(Button(label="Vendeur", style=discord.ButtonStyle.primary, custom_id="sell"))

    @discord.ui.button(label="Acheteur", style=discord.ButtonStyle.success, custom_id="buy")
    async def acheter(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TransactionModal("Acheteur"))

    @discord.ui.button(label="Vendeur", style=discord.ButtonStyle.primary, custom_id="sell")
    async def vendre(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TransactionModal("Vendeur"))

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne !")

@bot.command()
async def start(ctx):
    """Commande pour lancer le menu"""
    view = RoleSelectView()
    await ctx.send("Choisissez votre rôle :", view=view)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
