from rest_framework import serializers

from account.serializers import UserMeSerializer
from post.models import Post, PostAttachment, Comment, Trend


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'get_image']


class PostSerializer(serializers.ModelSerializer):
    created_by = UserMeSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count', 'created_at_formatted', 'created_by', 'attachments']


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserMeSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at_formatted', 'created_by']


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserMeSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count', 'created_at_formatted', 'created_by', 'comments', 'attachments']


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['id', 'hashtag', 'occurrences']
