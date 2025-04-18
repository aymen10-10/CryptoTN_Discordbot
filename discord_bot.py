import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

P2P_CHANNEL_ID = 123456789012345678  # Remplace par l'ID de ton salon #p2p
VENDEURS_CHANNEL_ID = 123456789012345679  # Remplace par l'ID du salon #liste-des-vendeurs
ACHETEURS_CHANNEL_ID = 123456789012345680  # Remplace par l'ID du salon #liste-des-acheteurs

# -------------------------- VUES INTERACTIVES --------------------------
class VenteAchatView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="vendre"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.secondary, custom_id="acheter"))


# -------------------------- FORMULAIRES --------------------------
class FormulaireVente(Modal, title="Créer une offre de vente"):
    montant = TextInput(label="Montant en USDT", placeholder="Ex: 100", required=True)
    prix = TextInput(label="Prix de vente (1 USDT = x DT)", placeholder="Ex: 3.2", required=True)
    methode = Select(
        placeholder="Choisis la méthode de paiement",
        options=[
            discord.SelectOption(label="D17"),
            discord.SelectOption(label="Mandat minute"),
            discord.SelectOption(label="Flouci"),
            discord.SelectOption(label="Versement bancaire"),
            discord.SelectOption(label="Virement bancaire")
        ]
    )
    identifiant = TextInput(label="Identifiant de paiement", placeholder="Ex: d17_aymen", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nouvelle offre de vente", color=discord.Color.green())
        embed.add_field(name="Vendeur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant disponible", value=f"{self.montant.value} USDT", inline=False)
        embed.add_field(name="Prix de vente", value=f"1 USDT = {self.prix.value} DT", inline=False)
        embed.add_field(name="Méthode de paiement", value=self.methode.values[0], inline=False)
        embed.add_field(name="Identifiant de paiement", value=self.identifiant.value, inline=False)
        await interaction.client.get_channel(VENDEURS_CHANNEL_ID).send(embed=embed)
        await interaction.response.send_message("Offre publiée avec succès !", ephemeral=True)


class FormulaireAchat(Modal, title="Créer une demande d'achat"):
    montant = TextInput(label="Montant souhaité (en USDT)", placeholder="Ex: 50", required=True)
    prix = TextInput(label="Prix proposé (1 USDT = x DT)", placeholder="Ex: 3.1", required=True)
    methode = Select(
        placeholder="Choisis la méthode de paiement",
        options=[
            discord.SelectOption(label="D17"),
            discord.SelectOption(label="Mandat minute"),
            discord.SelectOption(label="Flouci"),
            discord.SelectOption(label="Versement bancaire"),
            discord.SelectOption(label="Virement bancaire")
        ]
    )
    identifiant = TextInput(label="Identifiant de paiement", placeholder="Ex: d17_aymen", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nouvelle demande d'achat", color=discord.Color.blue())
        embed.add_field(name="Acheteur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant souhaité", value=f"{self.montant.value} USDT", inline=False)
        embed.add_field(name="Prix proposé", value=f"1 USDT = {self.prix.value} DT", inline=False)
        embed.add_field(name="Méthode de paiement", value=self.methode.values[0], inline=False)
        embed.add_field(name="Identifiant de paiement", value=self.identifiant.value, inline=False)
        await interaction.client.get_channel(ACHETEURS_CHANNEL_ID).send(embed=embed)
        await interaction.response.send_message("Demande d'achat publiée !", ephemeral=True)


# -------------------------- GESTION DES CLICS --------------------------
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "vendre":
            await interaction.response.send_modal(FormulaireVente())
        elif interaction.data["custom_id"] == "acheter":
            await interaction.response.send_modal(FormulaireAchat())


# -------------------------- AU DÉMARRAGE --------------------------
@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté.")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    await channel.purge()
    await channel.send(
        "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une option ci-dessous :",
        view=VenteAchatView()
    )


# -------------------------- LANCEMENT DU BOT --------------------------
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
