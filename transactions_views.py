import discord
from discord.ui import View, Button

class StartTransactionView(View):
    def __init__(self, acheteur_id, timeout=600):
        super().__init__(timeout=timeout)
        self.acheteur_id = acheteur_id

    @discord.ui.button(label="J’ai payé", style=discord.ButtonStyle.success)
    async def jai_paye(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.acheteur_id:
            await interaction.response.send_message("Seul l’acheteur peut cliquer ici.", ephemeral=True)
            return
        await interaction.response.send_message("Paiement confirmé. En attente du vendeur...", ephemeral=True)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def annuler(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.acheteur_id:
            await interaction.response.send_message("Seul l’acheteur peut annuler.", ephemeral=True)
            return
        await interaction.response.send_message("Transaction annulée.", ephemeral=True)
        self.stop()
