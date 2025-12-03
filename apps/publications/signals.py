from django.db.models.signals import post_save
from django.dispatch import receiver

from publications.models import Topic
from publications.services.services import create_topic_in_neo4j

@receiver(post_save, sender = Topic)
def sync_topic_to_neo4j(sender, instance, created, **kwargs):
    create_topic_in_neo4j(instance.id)