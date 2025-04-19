# cryptoTN_p2p_bot.py
import os
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
P2P_CHANNEL_ID = int(os.getenv("P2P_CHANNEL_ID"))
VENDEURS_CHANNEL_ID = int(os.getenv("VENDEURS_CHANNEL_ID"))
ACHETEURS_CHANNEL_ID = int(os.getenv("ACHETEURS_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

offres = []

class OffresView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Je veux vendre", style=discord.ButtonStyle.green, custom_id="vendre"))
        self.add_item(Button(label="Je veux acheter", style=discord.ButtonStyle.red, custom_id="acheter"))

class OffreModal(Modal):
    def __init__(self, type_offre):
        super().__init__(title=f"Créer une offre {type_offre}")
        self.type_offre = type_offre
        self.montant = TextInput(label="Montant disponible (USDT)", required=True)
        self.prix = TextInput(label="Prix de 1 USDT (en DT)", required=True)
        self.methode = TextInput(label="Méthode de paiement (ex: D17, Flouci)", required=True)
        self.identifiant = TextInput(label="Votre identifiant (RedotPay, Skrill...)", required=True)
        self.add_item(self.montant)
        self.add_item(self.prix)
        self.add_item(self.methode)
        self.add_item(self.identifiant)

    async def on_submit(self, interaction: discord.Interaction):
        offre = {
            "user": interaction.user.name,
            "type": self.type_offre,
            "montant": self.montant.value,
            "prix": self.prix.value,
            "methode": self.methode.value,
            "identifiant": self.identifiant.value
        }
        offres.append(offre)
        message = (
            f"**{self.type_offre.upper()} - {interaction.user.mention}**\n"
            f"Montant dispo : {self.montant.value} USDT\n"
            f"Prix : {self.prix.value} DT\n"
            f"Méthode : {self.methode.value}\n"
            f"Identifiant : `{self.identifiant.value}`\n"
        )
        target_channel = bot.get_channel(VENDEURS_CHANNEL_ID if self.type_offre == "vente" else ACHETEURS_CHANNEL_ID)
        await target_channel.send(message)
        await interaction.response.send_message("Votre offre a été publiée !", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot lancé en tant que {bot.user.name}")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        await channel.purge(limit=100)
        await channel.send("**Bienvenue sur le P2P CryptoTN !**", view=OffresView())

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "vendre":
            await interaction.response.send_modal(OffreModal("vente"))
        elif interaction.data["custom_id"] == "acheter":
            await interaction.response.send_modal(OffreModal("achat"))

bot.run(TOKEN)
