from rest_framework import serializers

from user.models import User
from .models import Post, Like, Follower


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user_id', 'content', 'post_date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']

class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower']



