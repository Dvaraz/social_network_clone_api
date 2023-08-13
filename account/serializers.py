from rest_framework import serializers

from account.models import User


class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2']
