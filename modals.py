from discord.ui import Modal, TextInput
from discord import Interaction

class VenteModal(Modal):
    def __init__(self):
        super().__init__(title="Créer une offre de vente")

        self.montant = TextInput(label="Montant USDT", placeholder="Ex : 100", required=True)
        self.prix = TextInput(label="Prix (1 USDT = X DT)", placeholder="Ex : 3.2", required=True)
        self.methode = TextInput(label="Méthode de paiement", placeholder="D17, Flouci, etc.", required=True)
        self.identifiant = TextInput(label="Identifiant de paiement", placeholder="Ex : @monpseudo", required=True)

        self.add_item(self.montant)
        self.add_item(self.prix)
        self.add_item(self.methode)
        self.add_item(self.identifiant)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message("Offre de vente enregistrée !", ephemeral=True)


class AchatModal(Modal):
    def __init__(self):
        super().__init__(title="Créer une demande d'achat")

        self.montant = TextInput(label="Montant USDT", placeholder="Ex : 200", required=True)
        self.prix = TextInput(label="Prix souhaité", placeholder="Ex : 3.1", required=True)
        self.methode = TextInput(label="Méthode de paiement", placeholder="D17, Flouci, etc.", required=True)
        self.identifiant = TextInput(label="Votre identifiant", placeholder="Ex : @votrepseudo", required=True)

        self.add_item(self.montant)
        self.add_item(self.prix)
        self.add_item(self.methode)
        self.add_item(self.identifiant)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message("Demande d'achat enregistrée !", ephemeral=True)
