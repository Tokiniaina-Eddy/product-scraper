from flask import jsonify

class APIRoutes:
    def __init__(self, app, db_manager, scraper=None, translator=None):
        self.app = app
        self.db = db_manager
        self.scraper = scraper
        self.translator = translator
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/')
        def home():
            return "<h1>API Opérationnelle</h1>"

        @self.app.route('/<platform>')
        def get_products(platform):
            try:
                data = self.db.get_collection_data(platform.capitalize())
                return jsonify(data), 200
            except Exception as e:
                return jsonify({"erreur": str(e)}), 500

        @self.app.route('/scraping/walmart', methods=['GET'])
        def set_products():
            print(">>> 1. Appel de la route reçu")
            try:
                # ÉTAPE 1 : SCRAPING
                # On utilise 'objets_produits'
                objets_produits = self.scraper.fetch_products("cars Accesories")
                
                # CORRECTION ICI : Tu avais écrit 'objets' au lieu de 'objets_produits'
                print(f">>> 2. Scraping fini : {len(objets_produits)} produits trouvés")
                
                if not objets_produits or len(objets_produits) == 0:
                    return jsonify({
                        "status": "fail",
                        "message": "Le scraping a échoué : aucun produit trouvé par l'API."
                    }), 404

                # ÉTAPE 2 : PRÉPARATION
                produits_dicts = [p.to_dict() for p in objets_produits]
                print(">>> 3. Lancement de la traduction (cela peut être long)...")

                # ÉTAPE 3 : TRADUCTION
                produits_traduits = self.translator.traduire_produits(produits_dicts)
                print(">>> 4. Traduction terminée")
                
                if not produits_traduits:
                    return jsonify({
                        "status": "fail",
                        "message": "La traduction a échoué : l'IA n'a pas retourné de données."
                    }), 500

                # ÉTAPE 4 : SAUVEGARDE
                self.db.save_all(produits_traduits, 'Walmart')
                return jsonify({"message" : "Scraping Walmart réussi"}), 200

            except Exception as e:
                # TRÈS IMPORTANT : On affiche l'erreur dans le terminal pour débugger
                print(f"!!! CRASH DÉTECTÉ : {str(e)}")
                return jsonify({"erreur": str(e)}), 500