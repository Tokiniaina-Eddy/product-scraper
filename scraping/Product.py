from datetime import date
class Product:
    """Représente un produit Walmart."""
    def __init__(self, data):
        self.id = data.get("product_id")
        self.titre = data.get("title")
        self.description = data.get("description")
        self.prix = data.get("primary_offer", {}).get("offer_price", "prix non disponible")
        self.image = data.get("thumbnail")
        self.note = data.get("rating", "Pas d'avis")
        self.lien = data.get("product_page_url")
        self.avis = data.get("reviews")
        self.date_scraping = date.today().isoformat()

    def to_dict(self):
        """Retourne le produit sous forme de dictionnaire."""
        return self.__dict__