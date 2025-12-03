# ==========================================
# Question Queries
# ==========================================

CREATE_QUESTION_QUERY = """
    MATCH (user:User {id: $user_id})
    MERGE (question:Question {id: $question_id})
    SET question.timestamp = $timestamp
    MERGE (user)-[:ASKED]->(question)
    
    WITH question
    UNWIND $topic_ids AS topic_id
    MATCH (topic:Topic {id: topic_id})
    MERGE (question)-[:HAS_TOPIC]->(topic)
"""

# ==========================================
# Answer Queries
# ==========================================


CREATE_ANSWER_QUERY = """
    MATCH (user:User {id: $user_id})
    MATCH (question:Question {id: $question_id})
    MERGE (answer:Answer {id: $answer_id})
    SET answer.timestamp = $timestamp
    MERGE (user)-[:ANSWERED]->(answer)
    MERGE (answer)-[:ANSWERS]->(question)
"""

# ==========================================
# Topic Queries
# ==========================================

CREATE_TOPIC_QUERY = """
    MERGE (:Topic {id: $topic_id})
"""

CHECK_FOLLOW_TOPIC_STATUS_QUERY = """
    MATCH (:User {id: $user_id})-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    RETURN count(r) > 0 as is_following
"""

FOLLOW_TOPIC_QUERY = """
    MATCH (user:User {id: $user_id})
    MATCH (topic:Topic {id: $topic_id})
    MERGE (user)-[:INTERESTED_IN]->(topic)
"""

UNFOLLOW_TOPIC_QUERY = """
    MATCH (:User {id: $user_id})-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    DELETE r
"""

GET_TOPIC_FOLLOWERS_COUNT_QUERY = """
    MATCH (:User)-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    RETURN count(r) as count
"""

GET_TOPICS_FROM_QUESTION_QUERY = """
    MATCH (question:Question {id: $question_id})-[:HAS_TOPIC]->(topic: Topic)
    RETURN topic.id AS id
"""

GET_QUESTIONS_FROM_TOPIC_QUERY = """
    MATCH (question:Question)-[:HAS_TOPIC]->(topic:Topic {id: $topic_id})
    RETURN question.id AS id
"""

# ==========================================
# Vote Queries
# ==========================================

GET_ENTITY_VOTE_STATUS_QUERY = """
    MATCH (:User {id: $user_id})-[r:UPVOTED|DOWNVOTED]->(:{label} {id: $target_id})
    RETURN type(r) as status
"""

UPVOTE_ENTITY_QUERY = """
    MATCH (user:User {{id: $user_id}})
    MATCH (target:{label} {{id: $target_id}})
    OPTIONAL MATCH (user)-[dv:DOWNVOTED]->(target)
    DELETE dv
    MERGE (user)-[uv:UPVOTED]->(target)
    RETURN uv
"""

DOWNVOTE_ENTITY_QUERY = """
    MATCH (user:User {{id: $user_id}})
    MATCH (target:{label} {{id: $target_id}})
    OPTIONAL MATCH (user)-[uv:UPVOTED]->(target)
    DELETE uv
    MERGE (user)-[dv:DOWNVOTED]->(target)
    RETURN dv
"""

REMOVE_ENTITY_VOTE_QUERY = """
    MATCH (:User {{id: $user_id}})-[r:UPVOTED|DOWNVOTED]->(:{label} {{id: $target_id}})
    DELETE r
"""

GET_ENTITY_VOTE_STATUS_QUERY = """
    MATCH (:User {{id: $user_id}})-[r:UPVOTED|DOWNVOTED]->(:{label} {{id: $target_id}})
    RETURN type(r) as status
"""

GET_ENTITY_VOTE_COUNT_QUERY = """
    MATCH (target:{label} {{id: $target_id}})
    RETURN
        COUNT {{ (:User)-[:UPVOTED]->(target) }} AS upvotes,
        COUNT {{ (:User)-[:DOWNVOTED]->(target) }} AS downvotes
"""

# ==========================================
# Feed Queries
# ==========================================
GET_USER_FEED_QUERY = """
    MATCH (user:User {id: $user_id})
    
    OPTIONAL MATCH (user)-[:FOLLOWS]->(:User)-[:ASKED]->(q1:Question)
    OPTIONAL MATCH (user)-[:INTERESTED_IN]->(:Topic)<-[:HAS_TOPIC]-(q2:Question)
    
    WITH collect(q1) + collect(q2) AS questions, user
    UNWIND questions AS question
    
    WITH DISTINCT question, user
    WHERE NOT (user)-[:ASKED]->(question)
    
    ORDER BY question.timestamp DESC
    LIMIT 50
    
    RETURN question.id AS id
"""
