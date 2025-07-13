from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class TelegramTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'api_token', 'telegram_chat_id',)
        model = UserModel
