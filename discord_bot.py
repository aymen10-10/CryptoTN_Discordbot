import discord
from discord.ext import commands
from discord import app_commands
from views import SellerSelectionView, BuyerSelectionView
from modals import CreateOfferModal
from utils import load_database, save_database
from handlers import envoyer_transaction

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

P2P_CHANNEL_ID = 1362872233768517913
SELLERS_CHANNEL_ID = 1362603391427018913
BUYERS_CHANNEL_ID = 1362872515743191070

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    channel = bot.get_channel(P2P_CHANNEL_ID)
    if channel:
        view = View()
        view.add_item(discord.ui.Button(label="Je veux vendre", style=discord.ButtonStyle.success, custom_id="vendre"))
        view.add_item(discord.ui.Button(label="Je veux acheter", style=discord.ButtonStyle.danger, custom_id="acheter"))
        await channel.send("Bienvenue sur CryptoTN P2P ! Choisissez une option :", view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "vendre":
            await interaction.response.send_modal(CreateOfferModal("vendeur", handle_offer_submission))
        elif interaction.data["custom_id"] == "acheter":
            await interaction.response.send_modal(CreateOfferModal("acheteur", handle_offer_submission))

async def handle_offer_submission(interaction, offer_type, montant, prix, methode, identifiant):
    db = load_database()
    offer = {
        "user": interaction.user.name,
        "id": interaction.user.id,
        "amount": montant,
        "price": prix,
        "method": methode,
        "identifiant": identifiant
    }
    if offer_type == "vendeur":
        db["vendeurs"].append(offer)
        channel = bot.get_channel(SELLERS_CHANNEL_ID)
        if channel:
            await channel.send(f"NOUVELLE OFFRE VENDEUR :\n<@{interaction.user.id}> - {montant} USDT à {prix} DT\nMéthode : {methode} | ID : `{identifiant}`")
    elif offer_type == "acheteur":
        db["acheteurs"].append(offer)
        channel = bot.get_channel(BUYERS_CHANNEL_ID)
        if channel:
            await channel.send(f"NOUVELLE OFFRE ACHETEUR :\n<@{interaction.user.id}> - {montant} USDT à {prix} DT\nMéthode : {methode} | ID : `{identifiant}`")
    save_database(db)
    await interaction.response.send_message("Votre offre a été enregistrée et publiée !", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
