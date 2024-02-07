from input_handler import get_user_input
from api_handler import query_api
from map_visualizer import visualize_on_map

def main():
    adresse, limit = get_user_input()
    if adresse and limit:  # Assurer que l'adresse et la limite saisies sont valides
        data = query_api(adresse, limit)
        if data:
            visualize_on_map(data)

if __name__ == "__main__":
    main()