import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === Views ===
class ActionSelectionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SellButton())
        self.add_item(BuyButton())

class SellButton(Button):
    def __init__(self):
        super().__init__(label="Je veux vendre", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SellOfferModal())

class BuyButton(Button):
    def __init__(self):
        super().__init__(label="Je veux acheter", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BuyRequestModal())

# === Modals ===
class SellOfferModal(Modal, title="Créer une offre de vente"):
    def __init__(self):
        super().__init__()
        self.asset_type = Select(
            placeholder="Choisissez le solde ",
            options=[
                discord.SelectOption(label="USDT (TRC20)", value="usdt"),
                discord.SelectOption(label="RedotPay", value="redotpay")
            ],
            min_values=1, max_values=1
        )
        self.amount = TextInput(label="Montant en USDT", placeholder="Ex : 100", required=True)
        self.price = TextInput(label="Prix de vente (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
        self.method = Select(
            placeholder="Méthode de paiement",
            options=[
                discord.SelectOption(label="D17", value="D17"),
                discord.SelectOption(label="Flouci", value="Flouci"),
                discord.SelectOption(label="Mandat minute", value="Mandat minute"),
                discord.SelectOption(label="Versement bancaire", value="Versement bancaire"),
                discord.SelectOption(label="Virement bancaire", value="Virement bancaire")
            ],
            min_values=1, max_values=1
        )
        self.identifier = TextInput(label="Identifiant de paiement", placeholder="Ex : d17_aymen", required=True)
        self.add_item(self.asset_type)
        self.add_item(self.amount)
        self.add_item(self.price)
        self.add_item(self.method)
        self.add_item(self.identifier)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nouvelle offre de vente", color=0x00ff00)
        embed.add_field(name="Vendeur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant", value=f"{self.amount.value} USDT", inline=True)
        embed.add_field(name="Prix", value=f"1 USDT = {self.price.value} DT", inline=True)
        embed.add_field(name="Méthode de paiement", value=self.method.values[0], inline=True)
        embed.add_field(name="Identifiant", value=self.identifier.value, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)

class BuyRequestModal(Modal, title="Créer une demande d'achat"):
    def __init__(self):
        super().__init__()
        self.asset_type = Select(
            placeholder="Choisissez le solde",
            options=[
                discord.SelectOption(label="USDT (TRC20)", value="usdt"),
                discord.SelectOption(label="RedotPay", value="redotpay")
            ],
            min_values=1, max_values=1
        )
        self.amount = TextInput(label="Montant souhaité en USDT", placeholder="Ex : 50", required=True)
        self.price = TextInput(label="Prix proposé (1 USDT = x DT)", placeholder="Ex : 3.1", required=True)
        self.method = Select(
            placeholder="Méthode de paiement",
            options=[
                discord.SelectOption(label="D17", value="D17"),
                discord.SelectOption(label="Flouci", value="Flouci"),
                discord.SelectOption(label="Mandat minute", value="Mandat minute"),
                discord.SelectOption(label="Versement bancaire", value="Versement bancaire"),
                discord.SelectOption(label="Virement bancaire", value="Virement bancaire")
            ],
            min_values=1, max_values=1
        )
        self.add_item(self.asset_type)
        self.add_item(self.amount)
        self.add_item(self.price)
        self.add_item(self.method)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nouvelle demande d'achat", color=0x3498db)
        embed.add_field(name="Acheteur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant souhaité", value=f"{self.amount.value} USDT", inline=True)
        embed.add_field(name="Prix proposé", value=f"1 USDT = {self.price.value} DT", inline=True)
        embed.add_field(name="Méthode de paiement", value=self.method.values[0], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=False)

# === Auto-send menu on ready ===
@bot.event
async def on_ready():
    channel_id = YOUR_CHANNEL_ID_HERE  # Remplace par l'ID du salon #p2p
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(
            "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition ou publiez une offre :",
            view=ActionSelectionView()
        )
    print(f"Bot connecté en tant que {bot.user}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
