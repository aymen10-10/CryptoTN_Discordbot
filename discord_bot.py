import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Mémoire temporaire
notes = {}

# Affichage des 4 dispositions
class DispositionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DispositionButton("USDT (TRC20)"))
        self.add_item(DispositionButton("RedotPay"))
        self.add_item(DispositionButton("Neteller"))
        self.add_item(DispositionButton("Skrill"))

class DispositionButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**Offres disponibles pour {self.label} :**\n(Liste dynamique à venir...)", ephemeral=True)

# Dès que le bot démarre
@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne.")
    channel = discord.utils.get(bot.get_all_channels(), name="p2p")
    if channel:
        await channel.send("Bienvenue sur le marché P2P ! Choisissez une disposition :", view=DispositionView())

# Commande pour noter un utilisateur
@bot.command()
async def noter(ctx, membre: discord.Member, note: int):
    if note < 1 or note > 5:
        await ctx.send("Merci de donner une note entre 1 et 5.")
        return
    if membre.id not in notes:
        notes[membre.id] = []
    notes[membre.id].append(note)
    moyenne = sum(notes[membre.id]) / len(notes[membre.id])
    await ctx.send(f"Note ajoutée. Nouvelle moyenne pour {membre.mention} : {round(moyenne, 2)} ⭐")
    
    if len(notes[membre.id]) >= 5 and moyenne >= 4:
        role = discord.utils.get(ctx.guild.roles, name="Vendeur Vérifié")
        if role:
            await membre.add_roles(role)
            await ctx.send(f"{membre.mention} a reçu le rôle **Vendeur Vérifié**.")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
