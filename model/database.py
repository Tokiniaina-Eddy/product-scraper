from pymongo import MongoClient

class DatabaseManager:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection_data(self, col_name):
        return list(self.db[col_name].find({}, {'_id': 0}))