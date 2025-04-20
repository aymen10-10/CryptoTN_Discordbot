from discord.ui import View, Button
from discord import ButtonStyle, Interaction
from discord import ButtonStyle

class StartTransactionView(View):
    def __init__(self, acheteur_id: int, vendeur_id: int, montant: float, method: str):
        super().__init__(timeout=600)  # 10 minutes
        self.acheteur_id = acheteur_id
        self.vendeur_id = vendeur_id
        self.montant = montant
        self.method = method
        self.acheteur_confirme = False
        self.vendeur_confirme = False

        self.add_item(Button(label="J'ai payé", style=ButtonStyle.success, custom_id="acheteur_confirme"))
        self.add_item(Button(label="J'ai reçu le paiement", style=ButtonStyle.primary, custom_id="vendeur_confirme"))

    async def interaction_check(self, interaction: Interaction) -> bool:
        # Permet uniquement à l’acheteur et au vendeur d’interagir
        return interaction.user.id in [self.acheteur_id, self.vendeur_id]

    @discord.ui.button(label="J'ai payé", style=ButtonStyle.success, custom_id="acheteur_confirme")
    async def acheteur_confirme_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id == self.acheteur_id:
            self.acheteur_confirme = True
            await interaction.response.send_message("Paiement confirmé par l'acheteur.", ephemeral=True)
        else:
            await interaction.response.send_message("Tu n'es pas l'acheteur.", ephemeral=True)

        await self.check_release(interaction)

    @discord.ui.button(label="J'ai reçu le paiement", style=ButtonStyle.primary, custom_id="vendeur_confirme")
    async def vendeur_confirme_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id == self.vendeur_id:
            self.vendeur_confirme = True
            await interaction.response.send_message("Réception confirmée par le vendeur.", ephemeral=True)
        else:
            await interaction.response.send_message("Tu n'es pas le vendeur.", ephemeral=True)

        await self.check_release(interaction)

    async def check_release(self, interaction: Interaction):
        if self.acheteur_confirme and self.vendeur_confirme:
            await interaction.followup.send("Les deux parties ont confirmé. L'USDT peut maintenant être libéré par le bot.")
            self.stop()
