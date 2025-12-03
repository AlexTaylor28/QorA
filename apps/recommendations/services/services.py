from users.models import User
from publications.models import Topic
from core.clients import neo4j_client
from recommendations.cypher_queries import (
    RECOMMEND_USERS_QUERY, 
    RECOMMEND_TOPICS_QUERY
)

def get_user_recommendations(user_id):
    results = neo4j_client.execute_read_many(RECOMMEND_USERS_QUERY, {'user_id': user_id})
    recommended_ids = [record['id'] for record in results]
    users = list(User.objects.filter(id__in = recommended_ids))

    #users.sort(key=lambda x: recommended_ids.index(x.id))
    return users

def get_topic_recommendations(user_id):
    """
    Returns a list of Topic objects recommended for the given user_id
    based on topic co-occurrence in questions.
    """
    results = neo4j_client.execute_read_many(RECOMMEND_TOPICS_QUERY, {'user_id': user_id})
    topic_ids = [record['id'] for record in results]
    
    topics = list(Topic.objects.filter(id__in=topic_ids))
    topics.sort(key=lambda x: topic_ids.index(x.id))
    
    return topics