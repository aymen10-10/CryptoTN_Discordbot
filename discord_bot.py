import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

transactions = {}

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne !")

@bot.command()
async def test(ctx):
    await ctx.send("Le bot Discord fonctionne !")

@bot.command()
async def escrow(ctx, montant: float, acheteur: discord.Member, vendeur: discord.Member):
    if montant > 5000:
        await ctx.send("Montant maximum autorisé : 5000 USDT.")
        return

    # Calcul des commissions
    if montant < 10:
        com_acheteur = 1
        com_vendeur = 1
    elif 10 <= montant <= 100:
        com_acheteur = 2
        com_vendeur = 2
    elif 100 < montant <= 500:
        com_acheteur = 3
        com_vendeur = 3
    else:
        com_acheteur = round(montant * 0.005, 2)
        com_vendeur = round(montant * 0.005, 2)

    transaction_id = len(transactions) + 1
    transactions[transaction_id] = {
        "acheteur": acheteur.id,
        "vendeur": vendeur.id,
        "montant": montant,
        "com_acheteur": com_acheteur,
        "com_vendeur": com_vendeur,
        "status": "en attente"
    }

    await ctx.send(
        f"**Transaction #{transaction_id}** créée :\n"
        f"Acheteur : {acheteur.mention} | Vendeur : {vendeur.mention}\n"
        f"Montant : `{montant} USDT`\n"
        f"Commission Acheteur : `{com_acheteur} USDT` | Commission Vendeur : `{com_vendeur} USDT`\n"
        f"Statut : `En attente de paiement`\n\n"
        f"{vendeur.mention} peut utiliser `!lock {transaction_id}` pour bloquer les fonds."
    )

@bot.command()
async def lock(ctx, transaction_id: int):
    if transaction_id not in transactions:
        await ctx.send("ID de transaction invalide.")
        return

    tx = transactions[transaction_id]
    if ctx.author.id != tx["vendeur"]:
        await ctx.send("Seul le vendeur peut bloquer les fonds.")
        return

    if tx["status"] != "en attente":
        await ctx.send("Cette transaction n'est pas en attente.")
        return

    tx["status"] = "bloqué"
    await ctx.send(f"Fonds simulés comme bloqués pour la transaction #{transaction_id}. En attente de confirmation de l'acheteur avec `!confirm {transaction_id}`.")

@bot.command()
async def confirm(ctx, transaction_id: int):
    if transaction_id not in transactions:
        await ctx.send("ID de transaction invalide.")
        return

    tx = transactions[transaction_id]
    if ctx.author.id != tx["acheteur"]:
        await ctx.send("Seul l'acheteur peut confirmer la transaction.")
        return

    if tx["status"] != "bloqué":
        await ctx.send("Les fonds ne sont pas encore bloqués.")

    tx["status"] = "confirmé"
    await ctx.send(
        f"Transaction #{transaction_id} confirmée.\n"
        f"USDT libérés au vendeur après déduction des commissions."
    )

@bot.command()
async def cancel(ctx, transaction_id: int):
    if transaction_id not in transactions:
        await ctx.send("ID de transaction invalide.")
        return

    tx = transactions[transaction_id]
    if ctx.author.id not in [tx["acheteur"], tx["vendeur"]]:
        await ctx.send("Seul l'acheteur ou le vendeur peut annuler cette transaction.")
        return

    if tx["status"] == "confirmé":
        await ctx.send("Transaction déjà confirmée. Trop tard pour annuler.")
        return

    tx["status"] = "annulée"
    await ctx.send(f"Transaction #{transaction_id} annulée avec succès.")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
