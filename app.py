from flask import Flask, jsonify, request
import pandas as pd
from pymongo import MongoClient
import os
from flask_cors import CORS



MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['SmartAutoCommerce']

def collection(col:str):
    collection = db[col]
    df = pd.DataFrame(list(collection.find()))
    if '_id' in df.columns:        
        df = df.drop(columns=['_id'])
    return df.to_dict(orient="records")

app = Flask(__name__)
CORS(app)
@app.route('/Amazon')
def amazon_product():
    try:
        return jsonify(collection("Amazon")), 200
    except Exception as e:
        return jsonify ({'statut':'erreur', 'erreur' : str(e)}), 500
@app.route('/walmart')
def walmart_product():
    try:
        return jsonify(collection("Walmart")), 200
    except Exception as e:
        return jsonify ({'statut':'erreur', 'erreur' : str(e)}), 500

@app.route('/')
def home():
    return "<h1>Bonjour</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

>