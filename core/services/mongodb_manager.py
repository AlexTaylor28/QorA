import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class MongoDBManager:
    
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri, database_name):
        if self._initialized:
            logger.info(f"[MongoDB Driver] Client already initialized for {self.uri}")
            return

        self.uri = uri
        self.database_name = database_name

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            print(f"[MongoDB Driver] Client configured for {self.uri}")
        except Exception as e:
            print(f"[MongoDB Driver] Could not configure MongoDB client: {e}")

        self._initialized = True

    def find_one(self, collection, filter = None):
        return self.db[collection].find_one(filter or {})

    def find_many(self, collection, filter = None, limit = 0):
        return list(self.db[collection].find(filter or {}).limit(limit))

    def insert_one(self, collection, document):
        return self.db[collection].insert_one(document).inserted_id

    def insert_many(self, collection, documents):
        return self.db[collection].insert_many(documents).inserted_ids

    def update_one(self, collection, filter, update):
        return self.db[collection].update_one(filter, update)

    def delete_one(self, collection, filter):
        return self.db[collection].delete_one(filter)

    def close(self):
        self.client.close()
        print(f"INFO: MongoDB Client closed for {self.uri}")
