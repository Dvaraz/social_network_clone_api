from rest_framework import serializers

from account.models import User, FriendshipRequest


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'friends_count', 'posts_count', 'get_avatar', ]


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserMeSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'created_by']


