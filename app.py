import os
from flask import Flask
from flask_cors import CORS
from app.database import DatabaseManager
from app.routes import APIRoutes
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialisation de la base de données
    mongo_uri = os.getenv("MONGO_URI")
    db_manager = DatabaseManager(mongo_uri, 'SmartAutoCommerce')

    # Initialisation des routes
    APIRoutes(app, db_manager)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)