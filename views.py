import discord
from discord.ui import View, Button
from actions import show_sellers, show_buyers

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SellerButton())
        self.add_item(BuyerButton())

class SellerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux vendre", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await show_sellers(interaction)

class BuyerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux acheter", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await show_buyers(interaction)

class StartTransactionView(discord.ui.View):
    def __init__(self, buyer_id, offre):
        super().__init__(timeout=600)  # 10 minutes
        self.buyer_id = buyer_id
        self.offre = offre
        self.confirmed = False

        self.add_item(Button(label="J’ai payé", style=discord.ButtonStyle.primary, custom_id="paiement"))
        self.add_item(Button(label="Annuler", style=discord.ButtonStyle.danger, custom_id="annuler"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.buyer_id

    async def on_timeout(self):
        if not self.confirmed:
            await self.message.edit(content="**Temps écoulé. La transaction a été annulée automatiquement.**", view=None)
