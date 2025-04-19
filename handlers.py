import discord
from discord.ext import commands
from discord.ui import View
from views import TransactionView
from utils import load_database, save_database, generate_transaction_id

def enregistrer_transaction(buyer_id, seller_id, amount):
    db = load_database()
    transaction_id = generate_transaction_id()
    db['transactions'][transaction_id] = {
        "buyer": buyer_id,
        "seller": seller_id,
        "amount": amount,
        "status": "en attente de paiement"
    }
    save_database(db)
    return transaction_id

async def envoyer_transaction(bot, channel_id, buyer_id, seller_id, amount):
    transaction_id = enregistrer_transaction(buyer_id, seller_id, amount)
    channel = bot.get_channel(channel_id)
    if not channel:
        return
    view = TransactionView(buyer=buyer_id, seller=seller_id, amount=amount, transaction_id=transaction_id)
    message = await channel.send(
        f"[EN COURS] Nouvelle transaction lancée entre <@{buyer_id}> et <@{seller_id}> pour {amount} USDT.",
        view=view
    )
    view.message = message
