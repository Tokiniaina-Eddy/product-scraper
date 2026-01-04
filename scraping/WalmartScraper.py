import requests
from datetime import date
from .Product import Product

class WalmartScraper:
    """Gère les recherches sur Walmart via SerpApi."""
    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_products(self, query, num=50):
        """Effectue la requête et retourne une liste d'objets Product."""
        params = {
            "api_key": self.api_key,
            "engine": "walmart",
            "location": "United States",
            "query": query,
            "sort": "best_seller",
            "num": str(num),
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status() # Vérifie si la requête a réussi
            data = response.json()
            
            if "organic_results" not in data:
                print("Aucun produit trouvé ou erreur API.")
                return []

            # Transformation des résultats bruts en objets Product
            return [Product(item) for item in data["organic_results"]]

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return []
