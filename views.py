from discord.ui import View, Button, Modal, TextInput
import discord

class P2PMainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="vendre"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="acheter"))
