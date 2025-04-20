import json
from discord import Interaction
from utils import load_database
from handlers import envoyer_offre_vendeur, envoyer_offre_acheteur, start_transaction

async def show_sellers(interaction: Interaction):
    db = load_database()
    sellers = db.get("vendeurs", [])
    if not sellers:
        await interaction.response.send_message("Aucun vendeur disponible.", ephemeral=True)
        return

    await interaction.response.send_message("Liste des vendeurs :", ephemeral=True)

async def show_buyers(interaction: Interaction):
    db = load_database()
    buyers = db.get("acheteurs", [])
    if not buyers:
        await interaction.response.send_message("Aucun acheteur disponible.", ephemeral=True)
        return

    await interaction.response.send_message("Liste des acheteurs :", ephemeral=True)

async def envoyer_offre_vendeur(interaction: Interaction, offre: dict):
    view = discord.ui.View(timeout=600)
    button = discord.ui.Button(label="Démarrer la transaction", style=discord.ButtonStyle.green)

    async def start(interaction2: Interaction):
        await start_transaction(interaction2, offre)

    button.callback = start
    view.add_item(button)
    await interaction.response.send_message(
        f"Offre de {offre['username']} - {offre['amount']} USDT à {offre['price']} DT", view=view, ephemeral=True
    )

async def envoyer_offre_acheteur(interaction: Interaction, offre: dict):
    view = discord.ui.View(timeout=600)
    button = discord.ui.Button(label="Démarrer la transaction", style=discord.ButtonStyle.green)

    async def start(interaction2: Interaction):
        await start_transaction(interaction2, offre)

    button.callback = start
    view.add_item(button)
    await interaction.response.send_message(
        f"Offre de {offre['username']} - {offre['amount']} USDT à {offre['price']} DT", view=view, ephemeral=True
    )

async def start_transaction(interaction: Interaction, offre: dict):
    await interaction.response.send_message(
        f"Transaction lancée avec {offre['username']} pour {offre['amount']} USDT à {offre['price']} DT.",
        ephemeral=True
    )
