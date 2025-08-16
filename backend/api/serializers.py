from django.contrib.auth import get_user_model
from rest_framework import serializers

from deck.models import Deck

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = UserModel


class TelegramTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('api_token', 'telegram_chat_id',)
        model = UserModel


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField()
    winrate = serializers.IntegerField()
    cards_in_queue = serializers.IntegerField()

    class Meta:
        fields = ('deck_name', 'card_count', 'winrate', 'cards_in_queue')
        read_only_fields = ('__all__',)
        model = Deck
