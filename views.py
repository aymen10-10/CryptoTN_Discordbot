import discord
from discord.ui import View, Button

class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="sell"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="buy"))
