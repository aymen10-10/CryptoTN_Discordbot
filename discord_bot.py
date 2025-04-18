import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ======== Boutons de disposition ========
class DispositionButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Offres pour {self.label} à venir...", ephemeral=True)

# ======== Boutons Je veux vendre / acheter ========
class VendreButton(Button):
    def __init__(self):
        super().__init__(label="Je veux vendre", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(VenteModal())

class AcheterButton(Button):
    def __init__(self):
        super().__init__(label="Je veux acheter", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AchatModal())

# ======== Vue principale du menu ========
class DispositionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DispositionButton("USDT (TRC20)"))
        self.add_item(DispositionButton("RedotPay"))
        self.add_item(DispositionButton("Neteller"))
        self.add_item(DispositionButton("Skrill"))
        self.add_item(VendreButton())
        self.add_item(AcheterButton())

# ======== Formulaire de vente ========
class VenteModal(Modal, title="Créer une offre de vente"):
    montant = TextInput(label="Montant en USDT", placeholder="Ex : 100", required=True)
    prix = TextInput(label="Prix de vente (1 USDT = x DT)", placeholder="Ex : 3.2", required=True)
    methode = TextInput(label="Méthode de paiement", placeholder="Ex : D17, Flouci...", required=True)
    identifiant = TextInput(label="Identifiant de paiement", placeholder="Ex : d17_aymen", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        salon = discord.utils.get(interaction.guild.text_channels, name="p2p") or interaction.channel
        embed = discord.Embed(title="Nouvelle offre de vente", color=0x00ff00)
        embed.add_field(name="Vendeur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant disponible", value=f"{self.montant.value} USDT", inline=True)
        embed.add_field(name="Prix de vente", value=f"1 USDT = {self.prix.value} DT", inline=True)
        embed.add_field(name="Méthode de paiement", value=self.methode.value, inline=True)
        embed.add_field(name="Identifiant", value=self.identifiant.value, inline=False)
        await salon.send(embed=embed, view=AcheterInteraction(
            vendeur=interaction.user,
            prix_usdt=float(self.prix.value),
            identifiant=self.identifiant.value,
            methode=self.methode.value
        ))
        await interaction.response.send_message("Ton offre a été publiée avec succès !", ephemeral=True)

# ======== Formulaire d'achat ========
class AchatModal(Modal, title="Créer une demande d'achat"):
    montant = TextInput(label="Montant souhaité en USDT", placeholder="Ex : 50", required=True)
    prix = TextInput(label="Prix proposé (1 USDT = x DT)", placeholder="Ex : 3.1", required=True)
    methode = TextInput(label="Méthode de paiement", placeholder="Ex : D17, Skrill...", required=True)
    identifiant = TextInput(label="Votre identifiant de paiement", placeholder="Ex : flouci_user", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        salon = discord.utils.get(interaction.guild.text_channels, name="p2p") or interaction.channel
        embed = discord.Embed(title="Nouvelle demande d'achat", color=0x3498db)
        embed.add_field(name="Acheteur", value=interaction.user.mention, inline=False)
        embed.add_field(name="Montant souhaité", value=f"{self.montant.value} USDT", inline=True)
        embed.add_field(name="Prix proposé", value=f"1 USDT = {self.prix.value} DT", inline=True)
        embed.add_field(name="Méthode de paiement", value=self.methode.value, inline=True)
        embed.add_field(name="Identifiant", value=self.identifiant.value, inline=False)
        await salon.send(embed=embed, view=TransactionVenteInteraction(
            acheteur=interaction.user,
            prix_usdt=float(self.prix.value),
            identifiant=self.identifiant.value,
            methode=self.methode.value
        ))
        await interaction.response.send_message("Ta demande d'achat a été publiée avec succès !", ephemeral=True)

# ======== Interaction Acheter (à partir de l'annonce du vendeur) ========
class AcheterInteraction(View):
    def __init__(self, vendeur: discord.Member, prix_usdt: float, identifiant: str, methode: str):
        super().__init__(timeout=1200)
        self.vendeur = vendeur
        self.prix_usdt = prix_usdt
        self.identifiant = identifiant
        self.methode = methode

    @discord.ui.button(label="Acheter", style=discord.ButtonStyle.primary)
    async def acheter(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(MontantAchatModal(
            vendeur=self.vendeur,
            prix_usdt=self.prix_usdt,
            identifiant=self.identifiant,
            methode=self.methode
        ))

class MontantAchatModal(Modal, title="Montant à acheter (USDT)"):
    montant = TextInput(label="Montant", placeholder="Ex : 50", required=True)

    def __init__(self, vendeur, prix_usdt, identifiant, methode):
        super().__init__()
        self.vendeur = vendeur
        self.prix_usdt = float(prix_usdt)
        self.identifiant = identifiant
        self.methode = methode

    async def on_submit(self, interaction: discord.Interaction):
        montant = float(self.montant.value)
        total_dt = montant * self.prix_usdt
        embed = discord.Embed(title="Transaction en cours", color=0xffc107)
        embed.add_field(name="Acheteur", value=interaction.user.mention, inline=True)
        embed.add_field(name="Vendeur", value=self.vendeur.mention, inline=True)
        embed.add_field(name="Montant", value=f"{montant} USDT", inline=False)
        embed.add_field(name="Total", value=f"{total_dt:.2f} DT", inline=True)
        embed.add_field(name="Méthode", value=self.methode, inline=True)
        embed.add_field(name="Identifiant", value=self.identifiant, inline=False)
        embed.set_footer(text="Transaction expirera dans 20 minutes.")
        await interaction.channel.send(embed=embed, view=TransactionActions())

# ======== Interaction Vente (à partir d'une demande d'achat) ========
class TransactionVenteInteraction(View):
    def __init__(self, acheteur: discord.Member, prix_usdt: float, identifiant: str, methode: str):
        super().__init__(timeout=1200)
        self.acheteur = acheteur
        self.prix_usdt = prix_usdt
        self.identifiant = identifiant
        self.methode = methode

    @discord.ui.button(label="Vendre", style=discord.ButtonStyle.success)
    async def vendre(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(MontantVenteModal(
            acheteur=self.acheteur,
            prix_usdt=self.prix_usdt,
            identifiant=self.identifiant,
            methode=self.methode
        ))

class MontantVenteModal(Modal, title="Montant à vendre (USDT)"):
    montant = TextInput(label="Montant", placeholder="Ex : 50", required=True)

    def __init__(self, acheteur, prix_usdt, identifiant, methode):
        super().__init__()
        self.acheteur = acheteur
        self.prix_usdt = float(prix_usdt)
        self.identifiant = identifiant
        self.methode = methode

    async def on_submit(self, interaction: discord.Interaction):
        montant = float(self.montant.value)
        total_dt = montant * self.prix_usdt
        embed = discord.Embed(title="Transaction en cours (vente)", color=0x8e44ad)
        embed.add_field(name="Vendeur", value=interaction.user.mention, inline=True)
        embed.add_field(name="Acheteur", value=self.acheteur.mention, inline=True)
        embed.add_field(name="Montant", value=f"{montant} USDT", inline=False)
        embed.add_field(name="Total", value=f"{total_dt:.2f} DT", inline=True)
        embed.add_field(name="Méthode", value=self.methode, inline=True)
        embed.add_field(name="Identifiant", value=self.identifiant, inline=False)
        embed.set_footer(text="Transaction expirera dans 20 minutes.")
        await interaction.channel.send(embed=embed, view=TransactionActions())

# ======== Boutons de transaction ========
class TransactionActions(View):
    def __init__(self):
        super().__init__(timeout=1200)
        self.add_item(Button(label="J’ai payé", style=discord.ButtonStyle.success))
        self.add_item(Button(label="Confirmer", style=discord.ButtonStyle.primary))
        self.add_item(Button(label="Annuler", style=discord.ButtonStyle.danger))

# ======== Lancement du bot ========
@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne.")
    channel = discord.utils.get(bot.get_all_channels(), name="p2p")
    if channel:
        async for msg in channel.history(limit=10):
            if msg.author == bot.user:
                await msg.delete()
        await channel.send(
            "**Bienvenue sur le marché P2P CryptoTN !**\nChoisissez une disposition ou publiez une offre :",
            view=DispositionView()
        )

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
