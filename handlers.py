import discord
from discord.ext import commands
from views import StartTransactionView
import json

async def envoyer_offre_vendeur(bot, channel_id, vendeur_id, montant_usdt, prix, methode, identifiant):
    channel = bot.get_channel(channel_id)
    if not channel:
        print("Salon introuvable.")
        return

    embed = discord.Embed(
        title="Nouvelle offre de vente USDT",
        description=f"**Vendeur :** <@{vendeur_id}>\n**Montant disponible :** {montant_usdt} USDT\n**Prix :** 1 USDT = {prix} DT\n**Méthode de paiement :** {methode}\n**Identifiant :** `{identifiant}`",
        color=discord.Color.green()
    )

    view = StartTransactionView(vendeur_id, montant_usdt, prix, methode, identifiant)
    await channel.send(embed=embed, view=view)

    # Optionnel : enregistrer l'offre dans la base de données
    try:
        with open("database.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"vendeurs": [], "acheteurs": [], "transactions": []}

    data["vendeurs"].append({
        "vendeur": vendeur_id,
        "montant_disponible": montant_usdt,
        "prix": prix,
        "methode": methode,
        "identifiant": identifiant
    })

    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)
