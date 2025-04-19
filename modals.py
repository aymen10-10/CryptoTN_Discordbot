import discord
import json
from discord import Interaction
from utils import save_database
from views import SellerSelectionView, BuyerSelectionView

class CreateOfferModal(discord.ui.Modal):
    def __init__(self, offer_type):
        title = "Créer une offre de vente" if offer_type == "sell" else "Créer une offre d'achat"
        super().__init__(title=title)
        self.offer_type = offer_type

        self.add_item(discord.ui.InputText(label="Montant (USDT)", placeholder="Ex: 100"))
        self.add_item(discord.ui.InputText(label="Prix (DT)", placeholder="Ex: 3.2"))
        self.add_item(discord.ui.InputText(label="Méthode de paiement", placeholder="Ex: D17, Flouci..."))

    async def callback(self, interaction: Interaction):
        username = interaction.user.name
        amount = self.children[0].value
        price = self.children[1].value
        method = self.children[2].value

        new_offer = {
            "username": username,
            "amount": amount,
            "price": price,
            "methode": method
        }

        # Charger les données existantes
        try:
            with open("database.json", "r") as f:
                db = json.load(f)
        except FileNotFoundError:
            db = {"sell_offers": [], "buy_offers": []}

        if self.offer_type == "sell":
            db["sell_offers"].append(new_offer)
        else:
            db["buy_offers"].append(new_offer)

        save_database(db)

        # Afficher les offres après ajout
        if self.offer_type == "sell":
            view = SellerSelectionView()
            await interaction.response.send_message("Offre de vente ajoutée :", view=view, ephemeral=True)
        else:
            view = BuyerSelectionView()
            await interaction.response.send_message("Offre d'achat ajoutée :", view=view, ephemeral=True)
