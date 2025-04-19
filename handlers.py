from views import StartTransactionView  # en haut du fichier

# Exemple d'envoi d'offre de vente (à adapter à ton code actuel)
view = StartTransactionView(vendeur_id=vendeur_id, montant_usdt=montant, prix=prix, methode=methode, identifiant=identifiant)
await channel.send(embed=embed, view=view)
