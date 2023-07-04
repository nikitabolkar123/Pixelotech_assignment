from django.db import models
from django.contrib.auth.models import AbstractUser

from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_likes')


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
