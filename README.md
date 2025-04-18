# CryptoTN P2P Discord Bot

Un bot Discord interactif pour faciliter les transactions P2P crypto (inspiré du système Binance P2P), avec :

- Interface à boutons : "Je veux vendre", "Je veux acheter"
- Formulaires de dépôt d'offres
- Affichage automatique dans des salons dédiés
- Configuration simple via `.env`
- Hébergement sur Railway

## Variables d'environnement à définir

- `DISCORD_TOKEN` : le token de ton bot Discord
- `P2P_CHANNEL_ID` : ID du salon #p2p
- `VENDEURS_CHANNEL_ID` : ID du salon #liste-des-vendeurs
- `ACHETEURS_CHANNEL_ID` : ID du salon #liste-des-acheteurs

## Lancer le bot en local

```bash
pip install -r requirements.txt
python bot.py
