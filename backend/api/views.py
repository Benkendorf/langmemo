from django.shortcuts import render
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import TelegramTokenSerializer

UserModel = get_user_model()


class UserModelViewSet(UserViewSet):
    queryset = UserModel.objects.all().order_by('username')
    #serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    @action(detail=True, methods=['post'],
            url_path='tg_token')
    def tg_token(self, request):
        pass
        # POST
        # Найти юзера по токену
        # Установить новый тг айди
        # Передать данные юзера в сериализатор

# При каждом запросе кроме установки токена проверять, что юзер с текущим тг чат айди есть в БД
