# Gère les entrées utilisateur (saisie de l'adresse et du nombre de résultats souhaités).

def get_user_input():
    while True:  # Démarre une boucle infinie qui continuera jusqu'à ce qu'une adresse valide soit saisie
        adresse = input("Veuillez saisir l'adresse (numéro et rue) : ")
        # Vérifie si l'adresse commence par un numéro
        if adresse.split()[0].isdigit():
            limit = input("Veuillez saisir le nombre de villes maximum recherchées : ")
            return adresse, limit
        else:
            print("L'adresse doit commencer par un numéro. Veuillez réessayer.")