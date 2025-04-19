import discord

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SellerButton())
        self.add_item(BuyerButton())

class SellerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux vendre", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        from handlers import show_sellers
        await show_sellers(interaction)

class BuyerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Je veux acheter", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        from handlers import show_buyers
        await show_buyers(interaction)
