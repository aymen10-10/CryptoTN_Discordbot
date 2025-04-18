import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Boutons principaux
class SaleDispositionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="sell"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="buy"))

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    try:
        channel_id = int(os.getenv("P2P_CHANNEL_ID"))
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.purge(limit=100)
            view = SaleDispositionView()
            await channel.send(
                "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition ou publiez une offre :",
                view=view
            )
        else:
            print("Salon P2P introuvable. Vérifie l'ID ou les permissions du bot.")
    except Exception as e:
        print(f"Erreur dans on_ready: {e}")

# Gestion des clics sur les boutons
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "sell":
            await interaction.response.send_modal(SellModal())
        elif interaction.data["custom_id"] == "buy":
            await interaction.response.send_modal(BuyModal())

# Formulaire de vente
class SellModal(Modal, title="Créer une offre de vente"):
    montant = TextInput(label="Montant en USDT", placeholder="Ex : 100", required=True)
    prix = TextInput(label="Prix de vente (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
    methode = TextInput(label="Méthode de paiement", placeholder="Ex : D17, Flouci...", required=True)
    identifiant = TextInput(label="Identifiant de paiement", placeholder="Ex : d17_aymen", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"**Nouvelle offre de vente**\n"
            f"Vendeur: {interaction.user.mention}\n"
            f"Montant disponible: {self.montant.value} USDT\n"
            f"Prix: 1 USDT = {self.prix.value} DT\n"
            f"Méthode de paiement: {self.methode.value}\n"
            f"Identifiant: {self.identifiant.value}",
            ephemeral=False
        )

# Formulaire d'achat
class BuyModal(Modal, title="Créer une demande d'achat"):
    montant = TextInput(label="Montant souhaité (en USDT)", placeholder="Ex : 50", required=True)
    prix = TextInput(label="Prix proposé (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
    methode = TextInput(label="Méthode de paiement", placeholder="Ex : D17, Flouci...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"**Nouvelle demande d'achat**\n"
            f"Acheteur: {interaction.user.mention}\n"
            f"Montant souhaité: {self.montant.value} USDT\n"
            f"Prix proposé: 1 USDT = {self.prix.value} DT\n"
            f"Méthode de paiement: {self.methode.value}",
            ephemeral=False
        )

# Exécution du bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
