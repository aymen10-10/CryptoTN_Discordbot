import discord
from discord.ui import Modal, InputText
import json
from views import StartTransactionView

def load_offers():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"vendeurs": [], "acheteurs": []}

def save_offers(data):
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)

class OffreVenteModal(Modal):
    def __init__(self):
        super().__init__(title="Nouvelle offre de vente")
        self.add_item(InputText(label="Montant disponible (USDT)", placeholder="Ex: 100"))
        self.add_item(InputText(label="Prix de vente (1 USDT en DT)", placeholder="Ex: 3.2"))
        self.add_item(InputText(label="Méthode de paiement", placeholder="Ex: D17"))
        self.add_item(InputText(label="Identifiant (RedotPay / Neteller / ...)", placeholder="Ex: Aymen123"))

    async def callback(self, interaction: discord.Interaction):
        montant = self.children[0].value
        prix = self.children[1].value
        methode = self.children[2].value
        identifiant = self.children[3].value

        offre = {
            "vendeur": interaction.user.id,
            "nom": interaction.user.name,
            "montant": montant,
            "prix": prix,
            "methode": methode,
            "identifiant": identifiant
        }

        data = load_offers()
        data["vendeurs"].append(offre)
        save_offers(data)

        embed = discord.Embed(
            title="VENTE - @" + interaction.user.name,
            description=(
                f"Montant dispo : {montant} USDT\n"
                f"Prix : {prix} DT\n"
                f"Méthode : {methode}\n"
                f"Identifiant : {identifiant}"
            ),
            color=0xF1C40F
        )

        channel_id = int(os.getenv("VENDEURS_CHANNEL_ID"))
        channel = interaction.client.get_channel(channel_id)
        await channel.send(embed=embed, view=StartTransactionView(offre, interaction.user))

        await interaction.response.send_message("Offre de vente publiée !", ephemeral=True)

class OffreAchatModal(Modal):
    def __init__(self):
        super().__init__(title="Nouvelle demande d'achat")
        self.add_item(InputText(label="Montant souhaité (USDT)", placeholder="Ex: 50"))
        self.add_item(InputText(label="Prix proposé (1 USDT en DT)", placeholder="Ex: 3.1"))
        self.add_item(InputText(label="Méthode de paiement", placeholder="Ex: D17"))

    async def callback(self, interaction: discord.Interaction):
        montant = self.children[0].value
        prix = self.children[1].value
        methode = self.children[2].value

        offre = {
            "acheteur": interaction.user.id,
            "nom": interaction.user.name,
            "montant": montant,
            "prix": prix,
            "methode": methode
        }

        data = load_offers()
        data["acheteurs"].append(offre)
        save_offers(data)

        embed = discord.Embed(
            title="ACHAT - @" + interaction.user.name,
            description=(
                f"Montant souhaité : {montant} USDT\n"
                f"Prix proposé : {prix} DT\n"
                f"Méthode de paiement : {methode}"
            ),
            color=0x3498DB
        )

        channel_id = int(os.getenv("ACHETEURS_CHANNEL_ID"))
        channel = interaction.client.get_channel(channel_id)
        await channel.send(embed=embed)

        await interaction.response.send_message("Demande d'achat publiée !", ephemeral=True)
