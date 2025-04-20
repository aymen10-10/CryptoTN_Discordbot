import json
from discord import Interaction
from utils import load_database
from views import StartTransactionView

async def show_sellers(interaction: Interaction):
    db = load_database()
    methodes = [offre for offre in db["vendeurs"] if offre["methode"]]
    if not methodes:
        await interaction.response.send_message("Aucun vendeur disponible.", ephemeral=True)
        return

    await interaction.response.send_message("Sélectionnez un vendeur :", ephemeral=True)

async def show_buyers(interaction: Interaction):
    db = load_database()
    methodes = [offre for offre in db["acheteurs"] if offre["methode"]]
    if not methodes:
        await interaction.response.send_message("Aucun acheteur disponible.", ephemeral=True)
        return

    await interaction.response.send_message("Voici la liste des acheteurs disponibles :", ephemeral=True)

async def start_transaction(interaction: Interaction, offre: dict):
    await interaction.response.send_message(
        f"Transaction lancée avec {offre['username']} pour {offre['amount']} USDT à {offre['price']} DT.",
        ephemeral=True
    )

async def envoyer_offre_vendeur(interaction: Interaction, offre: dict):
    buyer_id = interaction.user.id
    view = StartTransactionView(buyer_id=buyer_id, offre=offre)
    await interaction.response.send_message("Offre trouvée !", view=view, ephemeral=True)

async def envoyer_offre_acheteur(interaction: Interaction, offre: dict):
    seller_id = interaction.user.id
    view = StartTransactionView(seller_id=seller_id, offre=offre)
    await interaction.response.send_message("Offre trouvée !", view=view, ephemeral=True)
