# Gère la requête à l'API et l'affichage des résultats.

import requests

def query_api(adresse, limit):
    url_base = "https://api-adresse.data.gouv.fr/search/"
    params = {'q': adresse, 'limit': limit}
    response = requests.get(url_base, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Vérifier s'il y a des adresses dans la réponse
        if data['features']:
            # Affichage des adresses trouvées avec un index
            print("\nListe des adresses trouvées :")
            for index, feature in enumerate(data['features'], start=1):
                adresse_complete = feature['properties']['label']
                code_postal = feature['properties']['postcode']
                ville = feature['properties']['city']
                print(f"{index}. Adresse: {adresse_complete}, Code Postal: {code_postal}, Ville: {ville}")
        else:
            print("Aucune adresse trouvée. Essayez avec des termes de recherche différents.")
            return None
        return data
    else:
        print("Erreur lors de la requête à l'API")
        return None

