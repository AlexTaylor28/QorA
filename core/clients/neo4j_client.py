from django.conf import settings
from ..services.neo4j_manager import Neo4jManager

neo4j_client = Neo4jManager(uri = settings.NEO4J_URL, user = settings.NEO4J_USER, password = settings.NEO4J_PASSWORD)