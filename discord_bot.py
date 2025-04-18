import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Données temporaires
user_offers = []  # Liste des offres publiées

# --------- Modal pour vendre ---------
class SellModal(Modal, title="Créer une offre de vente"):
    def __init__(self):
        super().__init__()
        self.amount = TextInput(label="Montant en USDT", placeholder="Ex : 100", required=True)
        self.price = TextInput(label="Prix de vente (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
        self.method = Select(
            placeholder="Méthode de paiement",
            options=[
                discord.SelectOption(label="D17"),
                discord.SelectOption(label="Flouci"),
                discord.SelectOption(label="Versement bancaire"),
                discord.SelectOption(label="Virement bancaire"),
                discord.SelectOption(label="Mandat minute"),
            ],
            min_values=1,
            max_values=1
        )
        self.identifier = TextInput(label="Identifiant de paiement", placeholder="Ex : d17_aymen", required=True)

        self.add_item(self.amount)
        self.add_item(self.price)
        self.add_item(self.method)
        self.add_item(self.identifier)

    async def on_submit(self, interaction: discord.Interaction):
        offer = {
            "vendeur": interaction.user.mention,
            "montant": self.amount.value,
            "prix": self.price.value,
            "methode": self.method.values[0],
            "identifiant": self.identifier.value
        }
        user_offers.append(offer)
        await interaction.response.send_message(f"**Nouvelle offre de vente publiée :**\n"
                                              f"Vendeur : {offer['vendeur']}\n"
                                              f"Montant : {offer['montant']} USDT\n"
                                              f"Prix : 1 USDT = {offer['prix']} DT\n"
                                              f"Méthode : {offer['methode']}\n"
                                              f"Identifiant : {offer['identifiant']}",
                                              ephemeral=False)

# --------- Modal pour acheter ---------
class BuyModal(Modal, title="Créer une demande d'achat"):
    def __init__(self):
        super().__init__()
        self.amount = TextInput(label="Montant souhaité (en USDT)", placeholder="Ex : 50", required=True)
        self.price = TextInput(label="Prix proposé (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
        self.method = Select(
            placeholder="Méthode de paiement",
            options=[
                discord.SelectOption(label="D17"),
                discord.SelectOption(label="Flouci"),
                discord.SelectOption(label="Versement bancaire"),
                discord.SelectOption(label="Virement bancaire"),
                discord.SelectOption(label="Mandat minute"),
            ],
            min_values=1,
            max_values=1
        )

        self.add_item(self.amount)
        self.add_item(self.price)
        self.add_item(self.method)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**Nouvelle demande d'achat :**\n"
                                              f"Acheteur : {interaction.user.mention}\n"
                                              f"Montant souhaité : {self.amount.value} USDT\n"
                                              f"Prix proposé : 1 USDT = {self.price.value} DT\n"
                                              f"Méthode de paiement : {self.method.values[0]}",
                                              ephemeral=False)

# --------- Vue principale ---------
class P2PMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="sell"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.secondary, custom_id="buy"))

    @discord.ui.button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="sell")
    async def sell_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SellModal())

    @discord.ui.button(label="Je veux acheter", style=discord.ButtonStyle.secondary, custom_id="buy")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuyModal())

# --------- Lancement auto ---------
@bot.event
async def on_ready():
    channel_id = int(os.getenv("P2P_CHANNEL_ID"))
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.purge(limit=10)
        await channel.send("**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition ou publiez une offre :",
                           view=P2PMenu())
        print(f"Bot opérationnel : {bot.user.name}")

# --------- Token ---------
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
