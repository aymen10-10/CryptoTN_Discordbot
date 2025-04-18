def format_offer(user, montant, prix, methode, identifiant, role):
    return (
        f"{'Nouvelle offre de vente' if role == 'vendeur' else 'Nouvelle demande d’achat'}\n"
        f"Utilisateur : {user.mention}\n"
        f"Montant : {montant} USDT\n"
        f"Prix : 1 USDT = {prix} DT\n"
        f"Méthode : {methode}\n"
        f"Identifiant : {identifiant}"
    )
