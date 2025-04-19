import discord
from modals import CreateOfferModal
from utils import load_database
from actions import envoyer_offre_vendeur, envoyer_offre_acheteur, start_transaction

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SellerButton())
        self.add_item(BuyerButton())

class SellerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux vendre", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CreateOfferModal("sell"))

class BuyerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux acheter", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CreateOfferModal("buy"))

class SellerSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.populate_sellers()

    def populate_sellers(self):
        data = load_database()
        for offer in data.get("sell_offers", []):
            label = f"{offer['username']} - {offer['amount']} USDT - {offer['price']} DT"
            self.add_item(SellerSelectButton(label, offer))

class SellerSelectButton(discord.ui.Button):
    def __init__(self, label, offer):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.offer = offer

    async def callback(self, interaction: discord.Interaction):
        await envoyer_offre_vendeur(interaction, self.offer)

class BuyerSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.populate_buyers()

    def populate_buyers(self):
        data = load_database()
        for offer in data.get("buy_offers", []):
            label = f"{offer['username']} - {offer['amount']} USDT - {offer['price']} DT"
            self.add_item(BuyerSelectButton(label, offer))

class BuyerSelectButton(discord.ui.Button):
    def __init__(self, label, offer):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.offer = offer

    async def callback(self, interaction: discord.Interaction):
        await envoyer_offre_acheteur(interaction, self.offer)

class StartTransactionView(discord.ui.View):
    def __init__(self, offer):
        super().__init__(timeout=600)
        self.offer = offer
        self.add_item(StartTransactionButton(offer))

class StartTransactionButton(discord.ui.Button):
    def __init__(self, offer):
        super().__init__(label="Démarrer la transaction", style=discord.ButtonStyle.success)
        self.offer = offer

    async def callback(self, interaction: discord.Interaction):
        await start_transaction(interaction, self.offer)
