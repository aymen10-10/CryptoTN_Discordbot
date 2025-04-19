import discord
import asyncio
from discord.ui import View, Button

class StartTransactionView(View):
    def __init__(self, vendeur_id, montant_usdt, prix, methode, identifiant):
        super().__init__(timeout=600)  # 10 minutes
        self.vendeur_id = vendeur_id
        self.montant_usdt = montant_usdt
        self.prix = prix
        self.methode = methode
        self.identifiant = identifiant
        self.acheteur_id = None

    @discord.ui.button(label="Acheter cette offre", style=discord.ButtonStyle.green)
    async def acheter(self, interaction: discord.Interaction, button: Button):
        if self.acheteur_id is not None:
            await interaction.response.send_message("Cette offre est déjà en cours de transaction.", ephemeral=True)
            return
        self.acheteur_id = interaction.user.id

        montant_total = float(self.montant_usdt) * float(self.prix)
        await interaction.response.send_message(
            f"**Transaction lancée !**\nEnvoyez {montant_total:.2f} DT via {self.methode} vers : `{self.identifiant}`\n\nUne fois payé, cliquez sur 'J'ai payé'.",
            ephemeral=True,
            view=ConfirmPaymentView(self.vendeur_id, self.acheteur_id)
        )

class ConfirmPaymentView(View):
    def __init__(self, vendeur_id, acheteur_id):
        super().__init__(timeout=600)
        self.vendeur_id = vendeur_id
        self.acheteur_id = acheteur_id
        self.paye = False

    @discord.ui.button(label="J'ai payé", style=discord.ButtonStyle.blurple)
    async def jai_paye(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.acheteur_id:
            await interaction.response.send_message("Seul l'acheteur peut cliquer ici.", ephemeral=True)
            return
        self.paye = True
        await interaction.response.send_message(f"Paiement signalé. En attente de confirmation du vendeur.", ephemeral=True)

    @discord.ui.button(label="Libérer les fonds", style=discord.ButtonStyle.green)
    async def liberer(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.vendeur_id:
            await interaction.response.send_message("Seul le vendeur peut libérer les fonds.", ephemeral=True)
            return
        if not self.paye:
            await interaction.response.send_message("Le paiement n'a pas encore été signalé.", ephemeral=True)
            return
        await interaction.response.send_message("**Transaction complétée avec succès !** Merci pour votre confiance.", ephemeral=False)
        self.stop()
