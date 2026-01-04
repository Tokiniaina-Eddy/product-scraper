import os
from flask import Flask
from flask_cors import CORS
from model.database import DatabaseManager
from model.routes import APIRoutes
from scraping.Product import Product
from scraping.WalmartScraper import WalmartScraper
from scraping.Translator import TranslatorService
# from dotenv import load_dotenv


def create_app():
    # load_dotenv()
    app = Flask(__name__)
    CORS(app)

    # Initialisation de la base de données
    mongo_uri = os.getenv("MONGO_URI")
    serpapi = os.getenv("SERPAPI_KEY")
    gemini = os.getenv("API_G_KEY")
    db_manager = DatabaseManager(mongo_uri, 'SmartAutoCommerce')
    scraper = WalmartScraper(serpapi)
    translator = TranslatorService(gemini)

    # Initialisation des routes
    APIRoutes(app, db_manager, scraper, translator)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)