import json
from discord import Interaction
from utils import load_database
from handlers import envoyer_offre_vendeur

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
