import tkinter as tk
from tkinter import simpledialog, messagebox
import webbrowser
import requests

class ScrollableAddressList(tk.Toplevel):
    def __init__(self, parent, addresses):
        super().__init__(parent)
        self.title("Sélectionner une adresse")
        
        # Création d'un scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Création d'une listbox scrollable
        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        for address in addresses:
            self.listbox.insert(tk.END, address)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.listbox.yview)
        
        # Bouton de sélection
        select_button = tk.Button(self, text="Sélectionner", command=self.select_address)
        select_button.pack(pady=10)
        
        # Variable pour stocker l'adresse sélectionnée
        self.selected_address = None
    
    def select_address(self):
        try:
            index = self.listbox.curselection()[0]
            self.selected_address = self.listbox.get(index)
            self.destroy()  # Ferme la fenêtre après la sélection
        except IndexError:
            messagebox.showwarning("Attention", "Veuillez sélectionner une adresse.")
    
    def get_selected_address(self):
        self.wait_window(self)  # Attend que l'utilisateur fasse une sélection
        return self.selected_address


def query_api(adresse, limit):
    url_base = "https://api-adresse.data.gouv.fr/search/"
    params = {'q': adresse, 'limit': limit}
    try:
        response = requests.get(url_base, params=params)
        response.raise_for_status()  # Cela va déclencher une exception si le statut est un code d'erreur
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Erreur", "Erreur lors de la requête à l'API: " + str(e))
        return None

def visualize_on_map(data):
    if not data or 'features' not in data or not data['features']:
        messagebox.showinfo("Info", "Aucune donnée disponible pour visualisation.")
        return

    addresses = [f"{index+1}. {feature['properties']['label']}" for index, feature in enumerate(data['features'])]

    root = tk.Tk()  # Création d'une nouvelle instance Tk pour la fenêtre popup
    root.withdraw() 
    
    address_dialog = ScrollableAddressList(root, addresses)
    selected_address_str = address_dialog.get_selected_address()
    
    if selected_address_str:
        selected_number = int(selected_address_str.split('.')[0]) - 1
        feature = data['features'][selected_number]
        latitude = feature['geometry']['coordinates'][1]
        longitude = feature['geometry']['coordinates'][0]
        url_maps = f"https://www.google.com/maps?q={latitude},{longitude}"
        webbrowser.open_new_tab(url_maps)


def get_valid_address():
    while True:
        adresse = simpledialog.askstring("Adresse", "Veuillez saisir l'adresse (numéro et rue) :")
        if adresse is None:  # L'utilisateur a cliqué sur "Cancel"
            return None
        if adresse and adresse[0].isdigit():
            return adresse
        messagebox.showwarning("Attention", "L'adresse doit commencer par un numéro positif. Veuillez réessayer.")


def main():
    root = tk.Tk()
    root.withdraw()  # Nous n'avons pas besoin d'une fenêtre Tk,
    
    adresse = get_valid_address()
    limit = simpledialog.askinteger("Nombre de villes", "Veuillez saisir le nombre de villes maximum recherchées :", minvalue=1)
    if limit:
        data = query_api(adresse, limit)
        if data:
            visualize_on_map(data)
    
if __name__ == "__main__":
    main()
