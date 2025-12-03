from datetime import datetime
from core.clients.mongodb_client import mongodb_client
from bson import ObjectId
from users.models import User
from publications.models import Question

COLLECTION = 'notifications'

def create_notification(recipient_id, actor_id, verb, target_id = None, target_type = None):
    if recipient_id == actor_id:
        return

    notification = {
        'recipient_id': recipient_id,
        'actor_id': actor_id,
        'verb': verb,
        'target_id': target_id,
        'target_type': target_type,
        'is_read': False,
        'created_at': datetime.utcnow()
    }
    
    mongodb_client.insert_one(COLLECTION, notification)

def get_user_notifications(user_id, limit = 50):

    filter_query = {'recipient_id': user_id}
    sort_order = [('created_at', -1)]
    
    raw_notifs = mongodb_client.find_many(COLLECTION, filter_query, limit = limit, sort = sort_order)
    
    if not raw_notifs:
        return []

    actor_ids = set()
    question_ids = set()
    
    for n in raw_notifs:
        actor_ids.add(n.get('actor_id'))
        if n.get('target_type') == 'Question':
            question_ids.add(n.get('target_id'))
            
    users = {u.id: u for u in User.objects.filter(id__in=actor_ids)}
    questions = {q.id: q for q in Question.objects.filter(id__in=question_ids)}

    enriched_notifs = []
    for n in raw_notifs:
        n['id'] = str(n['_id'])
        n['actor'] = users.get(n['actor_id'])
        if n.get('target_type') == 'Question':  
            n['target'] = questions.get(n['target_id'])
        if n['actor']:
            enriched_notifs.append(n)

    return enriched_notifs

def mark_notification_as_read(notification_id):
    mongodb_client.update_one(
        COLLECTION,
        {'_id': ObjectId(notification_id)},
        {'$set': {'is_read': True}}
    )

def count_unread_notifications(user_id):
    return mongodb_client.count(COLLECTION, {'recipient_id': user_id, 'is_read': False})