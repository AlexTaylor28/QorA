from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Publication(models.Model):  

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "%(class)ss")
    content = models.TextField()
    timestamp = models.DateTimeField(default = timezone.now)
    is_approved = models.BooleanField(null = True, default = True) #CAMBIAR EL DEFAULT

    class Meta:
        abstract = True

    def set_vote_status(self, user_id):
        from publications.services.services import get_vote_status, get_vote_count

        label = self.__class__.__name__

        if user_id:
            self.user_vote_status = get_vote_status(user_id, self.id, label) or 'NONE'
        else:
            self.user_vote_status = 'NONE'
            
        upvotes, downvotes = get_vote_count(self.id, label)
        self.upvote_count = upvotes
        self.downvote_count = downvotes


class Topic(models.Model):

    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Question(Publication):
    
    title = models.CharField(max_length = 255)

    def __str__(self):
        return self.title

class Answer(Publication):

    question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'answers')  

    def __str__(self):
        return f"Answer to {self.question.title}"

