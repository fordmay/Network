from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="follows")

    def __str__(self):
        return f"{self.username}, id{self.pk}"


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user_like = models.ManyToManyField(User, blank=True, related_name="post_like")

    def __str__(self):
        return f"id:{self.pk}, owner:{self.owner}, time:{self.time}, likes:{self.user_like.all().count()}"
