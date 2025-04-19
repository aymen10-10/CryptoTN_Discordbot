from discord.ui import Modal, TextInput, View
from discord import Interaction
from utils import load_database
from actions import envoyer_offre_vendeur, envoyer_offre_acheteur

class CreateOfferModal(Modal):
    def __init__(self, offer_type):
        super().__init__(title="Créer une offre")
        self.offer_type = offer_type
        if offer_type == "sell":
            self.amount = TextInput(label="Montant en USDT", style=discord.TextStyle.short, required=True)
            self.price = TextInput(label="Prix en DT", style=discord.TextStyle.short, required=True)
            self.add_item(self.amount)
            self.add_item(self.price)
        elif offer_type == "buy":
            self.amount = TextInput(label="Montant en USDT", style=discord.TextStyle.short, required=True)
            self.price = TextInput(label="Prix en DT", style=discord.TextStyle.short, required=True)
            self.add_item(self.amount)
            self.add_item(self.price)

    async def on_submit(self, interaction: Interaction):
        if self.offer_type == "sell":
            await self.after_submit_sell(interaction)
        elif self.offer_type == "buy":
            await self.after_submit_buy(interaction)

    async def after_submit_sell(self, interaction: Interaction):
        from views import SellerSelectionView  # Import local
        db = load_database()
        offer = {
            "username": interaction.user.name,
            "amount": self.amount.value,
            "price": self.price.value,
            "methode": "D17",  # Ajoute ta méthode ici si nécessaire
        }
        db["vendeurs"].append(offer)
        view = SellerSelectionView()  # Crée la vue après avoir posté l'offre
        await interaction.response.send_message("Offre postée !", view=view, ephemeral=True)

    async def after_submit_buy(self, interaction: Interaction):
        from views import BuyerSelectionView  # Import local
        db = load_database()
        offer = {
            "username": interaction.user.name,
            "amount": self.amount.value,
            "price": self.price.value,
            "methode": "D17",  # Ajoute ta méthode ici si nécessaire
        }
        db["acheteurs"].append(offer)
        view = BuyerSelectionView()  # Crée la vue après avoir posté l'offre
        await interaction.response.send_message("Offre postée !", view=view, ephemeral=True)
