from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from users.services.services import create_user_in_neo4j
 
@receiver(post_save, sender = User)
def sync_user_to_neo4j(sender, instance, created, **kwargs):
    create_user_in_neo4j(instance.id)