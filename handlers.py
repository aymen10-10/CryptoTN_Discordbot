from discord import Interaction
import json
from utils import load_database

async def envoyer_offre_vendeur(interaction: Interaction, offre: dict):
    from views import StartTransactionView  # import local pour éviter boucle
    buyer_id = interaction.user.id
    view = StartTransactionView(buyer_id=buyer_id, offre=offre)
    await interaction.response.send_message("Offre trouvée !", view=view, ephemeral=True)
