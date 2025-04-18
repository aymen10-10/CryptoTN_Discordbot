import discord
from discord.ui import View
from modals import VenteModal, AchatModal

class ButtonHandlerView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="vendre"))
        self.add_item(discord.ui.Button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="acheter"))

    @discord.ui.button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="vendre")
    async def vendre_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VenteModal())

    @discord.ui.button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="acheter")
    async def acheter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AchatModal())
