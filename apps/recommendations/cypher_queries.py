# Suggest users that my followings follow, but I don't follow yet
# Logic: (Me) -> (Friend) -> (Stranger)
RECOMMEND_USERS_QUERY = """
    MATCH (user:User {id: $user_id})-[:FOLLOWS]->(friend:User)-[:FOLLOWS]->(recommended:User)
    WHERE NOT (user)-[:FOLLOWS]->(recommended) AND user.id <> recommended.id
    RETURN recommended.id AS id, count(friend) AS mutual_connections
    ORDER BY mutual_connections DESC
    LIMIT 5
"""

# Suggest topics related to topics I already follow
# Logic: (Me) -> (MyTopic) <- (Question) -> (RecommendedTopic)
# "People who asked about X also asked about Y" implies connection via Questions
RECOMMEND_TOPICS_QUERY = """
    MATCH (user:User {id: $user_id})-[:INTERESTED_IN]->(my_topic:Topic)<-[:HAS_TOPIC]-(q:Question)-[:HAS_TOPIC]->(rec_topic:Topic)
    WHERE NOT (user)-[:INTERESTED_IN]->(rec_topic) AND my_topic.id <> rec_topic.id
    RETURN rec_topic.id AS id, count(q) AS strength
    ORDER BY strength DESC
    LIMIT 5
"""