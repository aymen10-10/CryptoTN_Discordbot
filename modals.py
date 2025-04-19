import discord
from discord.ui import Modal, TextInput
from handlers import envoyer_offre_vendeur
import os

VENDEURS_CHANNEL_ID = int(os.getenv("VENDEURS_CHANNEL_ID"))

class FormulaireVente(Modal, title="Publier une offre de vente"):
    montant = TextInput(label="Montant en USDT", placeholder="Ex: 100", required=True)
    prix = TextInput(label="Prix (1 USDT = combien DT)", placeholder="Ex: 3.25", required=True)
    methode = TextInput(label="Méthode de paiement", placeholder="Ex: D17, Flouci, etc.", required=True)
    identifiant = TextInput(label="Votre identifiant de paiement", placeholder="Ex: Numéro D17, Flouci, etc.", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await envoyer_offre_vendeur(
            bot=interaction.client,
            channel_id=VENDEURS_CHANNEL_ID,
            vendeur_id=interaction.user.id,
            montant_usdt=self.montant.value,
            prix=self.prix.value,
            methode=self.methode.value,
            identifiant=self.identifiant.value
        )
        await interaction.response.send_message("Votre offre a été publiée avec succès !", ephemeral=True)
