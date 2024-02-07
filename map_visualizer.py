# Gère la visualisation d'une adresse sur une carte.

import webbrowser

def visualize_on_map(data):
    # Si aucune donnée n'est passée, rien à faire
    if not data or 'features' not in data or not data['features']:
        print("Aucune donnée disponible pour visualisation.")
        return

    # Demandez à l'utilisateur s'il souhaite visualiser une adresse sur une carte
    visualiser = input("Souhaitez-vous visualiser une adresse sur une carte ? (oui/non) : ")
    if visualiser.lower() in ['oui', 'o', 'yes', 'y']:
        num_adresse = int(input("Veuillez choisir le numéro de l'adresse à visualiser : ")) - 1
        
        if 0 <= num_adresse < len(data['features']):
            latitude = data['features'][num_adresse]['geometry']['coordinates'][1]
            longitude = data['features'][num_adresse]['geometry']['coordinates'][0]
            url_maps = f"https://www.google.com/maps?q={latitude},{longitude}"
            webbrowser.open_new_tab(url_maps)
            print(f"Ouverture de l'adresse dans Google Maps : {url_maps}")
        else:
            print("Numéro d'adresse invalide.")
    else:
        print("Visualisation annulée.")
