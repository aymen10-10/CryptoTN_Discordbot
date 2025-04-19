from discord.ui import Modal, InputText
from discord import InputTextStyle

class CreateOfferModal(Modal):
    def __init__(self, offer_type, on_submit_callback):
        super().__init__(title="Créer une offre")
        self.offer_type = offer_type
        self.on_submit_callback = on_submit_callback

        self.add_item(InputText(label="Montant (en USDT)", placeholder="Ex: 100"))
        self.add_item(InputText(label="Prix (1 USDT en DT)", placeholder="Ex: 3.2"))
        self.add_item(InputText(label="Méthode de paiement", placeholder="Ex: D17, Flouci..."))
        self.add_item(InputText(label="Identifiant paiement", placeholder="Ex: ton ID Redotpay, etc."))

    async def callback(self, interaction):
        montant = self.children[0].value
        prix = self.children[1].value
        methode = self.children[2].value
        identifiant = self.children[3].value

        await self.on_submit_callback(interaction, self.offer_type, montant, prix, methode, identifiant)
