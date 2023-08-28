from rest_framework import serializers

from account.serializers import UserMeSerializer
from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'body']

