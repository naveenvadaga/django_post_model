from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# enum class

class ReactionChoice(Enum):
    Like = "like"
    Love = "love"
    Haha = "haha"
    Wow = "wow"
    Sad = "sad"
    Angry = "angry"


# Create your models here.
class Person(AbstractUser):
    profilePicUrl = models.URLField(max_length=250, default="https://dummy.url.com/pic.png")


class React(models.Model):
    react_type = models.CharField(max_length=10,
                                  choices=[(reaction.value, reaction.value) for reaction in ReactionChoice])
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_at = models.DateTimeField(auto_now_add=True, blank=True)
    comment_content = models.CharField(max_length=100)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Post(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True, blank=True)
    post_content = models.CharField(max_length=100)
