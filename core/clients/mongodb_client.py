from django.conf import settings
from ..services.mongodb_manager import MongoDBManager

mongodb_client = MongoDBManager(uri = settings.MONGO_URL, database_name = settings.MONGO_DB)