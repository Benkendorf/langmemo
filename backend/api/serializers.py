from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = UserModel


class TelegramTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('api_token', 'telegram_chat_id',)
        model = UserModel
