from users.models import User
from core.clients import neo4j_client
from notifications.services.services import create_notification
from users.cypher_queries import (
    REGISTER_USER_QUERY,
    FOLLOW_USER_QUERY,
    UNFOLLOW_USER_QUERY,
    CHECK_FOLLOW_USER_STATUS_QUERY,
    GET_FOLLOWERS_QUERY,
    GET_FOLLOWERS_COUNT_QUERY,
    GET_FOLLOWING_QUERY,
    GET_FOLLOWING_COUNT_QUERY,
)

#TODO: MIRAR SI NECESITO DEVOLVER ALGO EN LAS QUERIES DE READ

def create_user_in_neo4j(user_id):
    neo4j_client.execute_write(REGISTER_USER_QUERY, { 'user_id': user_id })  
    
def follow_user(user_id, target_user_id):
    neo4j_client.execute_write(FOLLOW_USER_QUERY, {
        'user_id': user_id,
        'target_user_id': target_user_id
         })
    
    create_notification(
        recipient_id = target_user_id, 
        actor_id = user_id, 
        verb = 'followed_user'
    )
    
def unfollow_user(user_id, target_user_id):
    neo4j_client.execute_write(UNFOLLOW_USER_QUERY, {
        'user_id': user_id,
        'target_user_id': target_user_id
         })

def is_following_user(user_id, target_user_id) -> bool:
    record = neo4j_client.execute_read_one(CHECK_FOLLOW_USER_STATUS_QUERY, {
        'user_id': user_id,
        'target_user_id': target_user_id
    })
    return record['is_following']
       
def get_followers(user_id):
    results = neo4j_client.execute_read_many(GET_FOLLOWERS_QUERY, {'user_id': user_id})
    follower_ids = [record['id'] for record in results]
    return User.objects.filter(id__in = follower_ids)

def get_following(user_id):
    results = neo4j_client.execute_read_many(GET_FOLLOWING_QUERY, {'user_id': user_id})
    following_ids = [record['id'] for record in results]
    return User.objects.filter(id__in = following_ids)

def get_followers_count(user_id) -> int:
    result = neo4j_client.execute_read_one(GET_FOLLOWERS_COUNT_QUERY, {'user_id': user_id})
    return result['count']

def get_following_count(user_id) -> int:
    result = neo4j_client.execute_read_one(GET_FOLLOWING_COUNT_QUERY, {'user_id': user_id})
    return result['count']

