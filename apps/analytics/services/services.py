from core.clients.mongodb_client import get_mongo_db
from datetime import datetime

def log_page_view(user_id, path, ip_address):
    """
    Logs a page view event to MongoDB.
    """
    db = get_mongo_db()
    collection = db['page_views']
    
    event_data = {
        'user_id': user_id,
        'path': path,
        'ip_address': ip_address,
        'timestamp': datetime.utcnow()
    }
    
    # Insert directly into MongoDB
    collection.insert_one(event_data)

def get_page_views_count(path):
    """
    Example of reading from MongoDB
    """
    db = get_mongo_db()
    collection = db['page_views']
    return collection.count_documents({'path': path})