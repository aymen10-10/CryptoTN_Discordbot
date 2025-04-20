from transaction_views import StartTransactionView
from discord import Interaction
from views import StartTransactionView
from utils import load_database

async def envoyer_offre_vendeur(interaction: Interaction, offre: dict):
    buyer_id = interaction.user.id
    view = StartTransactionView(offer=offre)
    await interaction.response.send_message(
        "Offre trouvée ! Cliquez pour démarrer la transaction :",
        view=view,
        ephemeral=True
    )

async def envoyer_offre_acheteur(interaction: Interaction, offre: dict):
    seller_id = interaction.user.id
    view = StartTransactionView(offer=offre)
    await interaction.response.send_message(
        "Offre trouvée ! Cliquez pour démarrer la transaction :",
        view=view,
        ephemeral=True
    )
