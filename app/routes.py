from flask import jsonify

class APIRoutes:
    def __init__(self, app, db_manager):
        self.app = app
        self.db = db_manager
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/')
        def home():
            return "<h1>API Opérationnelle</h1>"

        @self.app.route('/<platform>')
        def get_products(platform):
            # platform devient "Amazon" ou "Walmart" selon l'URL
            try:
                data = self.db.get_collection_data(platform.capitalize())
                return jsonify(data), 200
            except Exception as e:
                return jsonify({"erreur": str(e)}), 500