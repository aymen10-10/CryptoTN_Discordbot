import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Select, Modal, TextInput
import asyncio
import os
intents = discord.Intents.default() intents.message_content = True bot = commands.Bot(command_prefix="!", intents=intents)

pending_transactions = {}

class RoleSelect(View): def init(self): super().init(timeout=None)

@discord.ui.button(label="Acheteur", style=discord.ButtonStyle.success)
async def acheteur(self, interaction: discord.Interaction, button: Button):
    await interaction.response.send_message("Liste des vendeurs disponibles :", view=UserSelect(role="vendeur"), ephemeral=True)

@discord.ui.button(label="Vendeur", style=discord.ButtonStyle.primary)
async def vendeur(self, interaction: discord.Interaction, button: Button):
    await interaction.response.send_message("Liste des acheteurs disponibles :", view=UserSelect(role="acheteur"), ephemeral=True)

class UserSelect(View): def init(self, role): super().init(timeout=None) self.add_item(UserDropdown(role))

class UserDropdown(Select): def init(self, role): self.role = role options = [ discord.SelectOption(label=member.display_name, value=str(member.id)) for member in []  # Tu peux ici filtrer les membres selon des critères si besoin ] if not options: options = [discord.SelectOption(label="Aucun utilisateur", value="none")]

super().__init__(placeholder=f"Choisir un {role}", min_values=1, max_values=1, options=options)

async def callback(self, interaction: discord.Interaction):
    if self.values[0] == "none":
        await interaction.response.send_message("Aucun utilisateur disponible.", ephemeral=True)
        return
    user_id = int(self.values[0])
    partenaire = interaction.guild.get_member(user_id)
    await interaction.response.send_modal(AmountModal(partenaire))

class AmountModal(Modal): def init(self, partenaire): super().init(title="Entrer le montant de la transaction") self.montant = TextInput(label="Montant (USDT)", placeholder="Ex: 100", required=True) self.partenaire = partenaire self.add_item(self.montant)

async def on_submit(self, interaction: discord.Interaction):
    try:
        montant = float(self.montant.value)
    except ValueError:
        await interaction.response.send_message("Montant invalide.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Transaction P2P en attente",
        description=f"Acheteur : {interaction.user.mention}\nVendeur : {self.partenaire.mention}\nMontant : {montant} USDT\nStatut : En attente de validation",
        color=discord.Color.orange()
    )
    view = TransactionValidation(interaction.user, self.partenaire, montant)
    message = await interaction.channel.send(embed=embed, view=view)

    view.message = message
    view.timeout_task.start()
    await interaction.response.send_message("Transaction initiée !", ephemeral=True)

class TransactionValidation(View): def init(self, acheteur, vendeur, montant): super().init(timeout=None) self.acheteur = acheteur self.vendeur = vendeur self.montant = montant self.message = None self.confirmed = False

@discord.ui.button(label="Confirmer", style=discord.ButtonStyle.success)
async def confirmer(self, interaction: discord.Interaction, button: Button):
    if interaction.user != self.vendeur:
        await interaction.response.send_message("Seul le vendeur peut confirmer.", ephemeral=True)
        return
    self.confirmed = True
    await interaction.response.send_message("Transaction confirmée. USDT libérés !")
    await self.message.edit(embed=discord.Embed(title="Transaction terminée", description=f"{self.montant} USDT envoyés à {self.acheteur.mention}.", color=discord.Color.green()), view=None)
    self.timeout_task.cancel()

@discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
async def annuler(self, interaction: discord.Interaction, button: Button):
    await self.message.edit(embed=discord.Embed(title="Transaction annulée", description="Cette transaction a été annulée.", color=discord.Color.red()), view=None)
    self.timeout_task.cancel()

@tasks.loop(count=1)
async def timeout_task(self):
    await asyncio.sleep(1200)  # 20 minutes
    if not self.confirmed:
        await self.message.edit(embed=discord.Embed(title="Transaction expirée", description="Délai de 20 minutes dépassé.", color=discord.Color.red()), view=None)

@bot.event async def on_ready(): print(f"{bot.user} est en ligne !")

@bot.command() async def p2p(ctx): await ctx.send("Bienvenue sur CryptoTN P2P ! Choisissez votre rôle :", view=RoleSelect())

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

