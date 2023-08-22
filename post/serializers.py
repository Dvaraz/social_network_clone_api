from rest_framework import serializers

from account.serializers import UserMeSerializer
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = UserMeSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count', 'created_at_formatted', 'created_by']
