
#MAYBE CHANGE TO CREATE_USER_QUERY??
REGISTER_USER_QUERY = """
    MERGE (:User {id: $user_id})
"""

FOLLOW_USER_QUERY = """
    MATCH (user:User {id: $user_id})
    MATCH (target_user:User {id: $target_user_id})
    MERGE (user)-[:FOLLOWS]->(target_user)
"""
    
UNFOLLOW_USER_QUERY = """
    MATCH (:User {id: $user_id})-[r:FOLLOWS]->(:User {id: $target_user_id})
    DELETE r
"""

CHECK_FOLLOW_USER_STATUS_QUERY = """
    MATCH (:User {id: $user_id})-[r:FOLLOWS]->(:User {id: $target_user_id})
    RETURN count(r) > 0 as is_following
"""

GET_FOLLOWERS_QUERY = """
    MATCH (target:User)-[:FOLLOWS]->(:User {id: $user_id})
    RETURN target.id as id
"""

GET_FOLLOWING_QUERY = """
    MATCH (:User {id: $user_id})-[:FOLLOWS]->(target:User)
    RETURN target.id as id
"""

GET_FOLLOWERS_COUNT_QUERY = """
    MATCH (:User)-[r:FOLLOWS]->(:User {id: $user_id})
    RETURN count(r) as count
"""

GET_FOLLOWING_COUNT_QUERY = """
    MATCH (:User {id: $user_id})-[r:FOLLOWS]->(:User)
    RETURN count(r) as count
"""