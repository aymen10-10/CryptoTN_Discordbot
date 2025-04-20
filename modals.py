import discord
import json
from utils import save_database

class CreateOfferModal(discord.ui.Modal):
    def __init__(self, offer_type: str):
        super().__init__(title="Nouvelle offre")
        self.offer_type = offer_type

        self.add_item(discord.ui.InputText(label="Montant en USDT"))
        self.add_item(discord.ui.InputText(label="Prix (1 USDT = ? DT)"))
        self.add_item(discord.ui.InputText(label="Méthode de paiement (ex: D17, Flouci, Virement)"))
        self.add_item(discord.ui.InputText(label="ID RedotPay ou infos de paiement"))

    async def callback(self, interaction: discord.Interaction):
        montant = self.children[0].value
        prix = self.children[1].value
        methode = self.children[2].value
        identifiant = self.children[3].value

        try:
            db = {}
            with open("database.json", "r", encoding="utf-8") as f:
                db = json.load(f)
        except FileNotFoundError:
            db = {"vendeurs": [], "acheteurs": []}

        offre = {
            "username": str(interaction.user),
            "amount": montant,
            "price": prix,
            "methode": methode,
            "id_paiement": identifiant
        }

        if self.offer_type == "sell":
            db["vendeurs"].append(offre)
            await interaction.response.send_message("Ton offre de vente a été enregistrée !", ephemeral=True)
        else:
            db["acheteurs"].append(offre)
            await interaction.response.send_message("Ton offre d’achat a été enregistrée !", ephemeral=True)

        save_database(db)
