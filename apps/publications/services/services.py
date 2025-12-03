from django.db import transaction
from core.clients import neo4j_client
from publications.models import Question, Answer, Topic
from publications.cypher_queries import (
    CREATE_QUESTION_QUERY,
    GET_USER_FEED_QUERY,
    CREATE_ANSWER_QUERY,

    CREATE_TOPIC_QUERY,
    GET_TOPICS_FROM_QUESTION_QUERY,
    GET_QUESTIONS_FROM_TOPIC_QUERY,
    CHECK_FOLLOW_TOPIC_STATUS_QUERY,
    FOLLOW_TOPIC_QUERY,
    UNFOLLOW_TOPIC_QUERY,
    GET_TOPIC_FOLLOWERS_COUNT_QUERY,

    GET_ENTITY_VOTE_STATUS_QUERY,
    UPVOTE_ENTITY_QUERY,
    DOWNVOTE_ENTITY_QUERY,
    REMOVE_ENTITY_VOTE_QUERY,
    GET_ENTITY_VOTE_COUNT_QUERY,
) 

# ==========================================
# Question Services
# ==========================================

@transaction.atomic
def create_question(user, title, content, topic_ids = None):

    question = Question.objects.create(
        user = user,
        title = title,
        content = content
    )

    neo4j_client.execute_write(CREATE_QUESTION_QUERY, {
        'user_id': user.id,
        'question_id': question.id,
        'topic_ids': topic_ids or [],
        'timestamp': question.timestamp.timestamp()
    })

    return question


def get_user_feed(user_id):

    results = neo4j_client.execute_read_many(GET_USER_FEED_QUERY, {'user_id': user_id})
    question_ids = [record['id'] for record in results]
    
    return Question.objects.filter(id__in = question_ids).order_by('-timestamp')

# ==========================================
# Answer Services
# ==========================================

@transaction.atomic
def create_answer(user, question_id, content):
    question = Question.objects.get(id = question_id)

    answer = Answer.objects.create(
        user = user,
        question = question,
        content = content
    )

    neo4j_client.execute_write(CREATE_ANSWER_QUERY, {
        'user_id': user.id,
        'question_id': question_id,
        'answer_id': answer.id,
        'timestamp': answer.timestamp.timestamp()
    })

    return answer

# ==========================================
# Topics Services
# ==========================================

#CALLED FROM SIGNAL
def create_topic_in_neo4j(topic_id):
    neo4j_client.execute_write(CREATE_TOPIC_QUERY, {'topic_id': topic_id})

def get_topics_from_question(question_id):
    results = neo4j_client.execute_read_many(GET_TOPICS_FROM_QUESTION_QUERY, {'question_id': question_id})
    topic_ids = [record['id'] for record in results]
    return Topic.objects.filter(id__in = topic_ids)

def get_questions_from_topic(topic_id):
    results = neo4j_client.execute_read_many(GET_QUESTIONS_FROM_TOPIC_QUERY, {'topic_id': topic_id})
    question_ids = [record['id'] for record in results]
    return Question.objects.filter(id__in = question_ids).order_by('-timestamp')

def is_following_topic(user_id, topic_id) -> bool:
    record = neo4j_client.execute_read_one(CHECK_FOLLOW_TOPIC_STATUS_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })
    return record['is_following']

def follow_topic(user_id, topic_id):
    neo4j_client.execute_write(FOLLOW_TOPIC_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })

def unfollow_topic(user_id, topic_id):
    neo4j_client.execute_write(UNFOLLOW_TOPIC_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })

def get_topic_followers_count(topic_id):
    result = neo4j_client.execute_read_one(GET_TOPIC_FOLLOWERS_COUNT_QUERY, {'topic_id': topic_id})
    return result['count']

# ==========================================
# Vote Services
# ==========================================

def get_vote_status(user_id, target_id, target_label):
    query = GET_ENTITY_VOTE_STATUS_QUERY.format(label = target_label)
    result = neo4j_client.execute_read_one(query, {
        'user_id': user_id, 
        'target_id': target_id
    })
    return result['status'] if result else None

def get_question_vote_status(user_id, question_id):
    return get_vote_status(user_id, question_id, "Question")

def get_answer_vote_status(user_id, answer_id):
    return get_vote_status(user_id, answer_id, "Answer")

def _execute_vote_action(query_template, user_id, target_id, target_label):
    query = query_template.format(label = target_label)
    neo4j_client.execute_write(query, {
            'user_id': user_id,
            'target_id': target_id
    })

def upvote_question(user_id, question_id):
    _execute_vote_action(UPVOTE_ENTITY_QUERY, user_id, question_id, "Question")

def downvote_question(user_id, question_id):
    _execute_vote_action(DOWNVOTE_ENTITY_QUERY, user_id, question_id, "Question")

def remove_question_vote(user_id, question_id):
    _execute_vote_action(REMOVE_ENTITY_VOTE_QUERY, user_id, question_id, "Question")
    
def upvote_answer(user_id, answer_id):
    _execute_vote_action(UPVOTE_ENTITY_QUERY, user_id, answer_id, "Answer")

def downvote_answer(user_id, answer_id):
    _execute_vote_action(DOWNVOTE_ENTITY_QUERY, user_id, answer_id, "Answer")

def remove_answer_vote(user_id, answer_id):
    _execute_vote_action(REMOVE_ENTITY_VOTE_QUERY, user_id, answer_id, "Answer")

def get_vote_count(target_id, target_label):
    query = GET_ENTITY_VOTE_COUNT_QUERY.format(label = target_label)
    result = neo4j_client.execute_read_one(query, {'target_id': target_id})
    return result['upvotes'], result['downvotes']
