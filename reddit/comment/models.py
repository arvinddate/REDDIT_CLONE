from django.db import models
from question_answer.models import Answer
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)
    image = models.ImageField(upload_to='comments', null=True, blank=True)
    added_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    def __str__(self):
        return str(self.comments)
    