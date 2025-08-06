import logging

from django.shortcuts import render, get_object_or_404
from djoser.views import UserViewSet
from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import TelegramTokenSerializer, UserSerializer
from deck.models import Card
from homepage.views import get_total_queue_end_of_day
from django_mem_cards.constants import (WEEKDAYS_RUS,
                                        TOTAL_CALENDAR_DAYS)

UserModel = get_user_model()


class UserModelViewSet(UserViewSet):
    queryset = UserModel.objects.all().order_by('username')
    permission_classes = [IsAdminUser, ]

    @action(detail=False, methods=['post'],
            url_path='tg_token')
    def tg_token(self, request):
        token_user = get_object_or_404(UserModel, api_token=request.data['api_token'])
        serializer = UserSerializer(token_user, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(
                status=status.HTTP_200_OK, data={'ligma': 'balls', 'sugandese': 'nuts'}
            )

    @action(detail=False, methods=['get'],
            url_path='get_info')
    def get_info(self, request):
        chat_user = get_object_or_404(UserModel, telegram_chat_id=request.data['telegram_chat_id'])

        cards_total_now = Card.objects.filter(
            deck__user=chat_user,
            in_queue=True
        ).count()

        if cards_total_now is None:
            cards_total_now = 0

        end_of_day_totals = [
            get_total_queue_end_of_day(plus_days=i, user=chat_user)
            for i in range(TOTAL_CALENDAR_DAYS)
        ]
        calendar = [
            {'weekday': 'Сегодня',
                'diff': end_of_day_totals[0] - cards_total_now,
                'end_of_day': end_of_day_totals[0]},
        ] + [
            {'weekday': WEEKDAYS_RUS[(timezone.now().weekday() + i) % 7],
                'diff': end_of_day_totals[i] - end_of_day_totals[i - 1],
                'end_of_day': end_of_day_totals[i]}
            for i in range(1, TOTAL_CALENDAR_DAYS)
        ]

        payload = {'calendar': calendar, 'cards_total_now': cards_total_now}

        return Response(
                status=status.HTTP_200_OK, data=payload
            )

    @action(detail=False, methods=['get'],
            url_path='get_decks', pagination_class=PageNumberPagination)
    def get_decks(self, request):
        chat_user = get_object_or_404(UserModel, telegram_chat_id=request.data['telegram_chat_id'])
        decks = chat_user.decks.annotate()
        page = self.paginate_queryset(decks)

        
