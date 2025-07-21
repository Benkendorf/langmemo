import logging

from django.shortcuts import render, get_object_or_404
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import TelegramTokenSerializer, UserSerializer

UserModel = get_user_model()


class UserModelViewSet(UserViewSet):
    queryset = UserModel.objects.all().order_by('username')
    #serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    @action(detail=False, methods=['post'],
            url_path='tg_token')
    def tg_token(self, request):
        #logging.critical(f'HEADERS: {dict(request.headers)}')
        logging.critical(request.data)
        token_user = get_object_or_404(UserModel, api_token=request.data['api_token'])
        serializer = UserSerializer(token_user, data=request.data, partial=True)
        serializer.is_valid()
        logging.critical('-----------------')
        logging.critical(serializer.errors)
        logging.critical('-----------------')
        serializer.save()
        return Response(
                status=status.HTTP_200_OK, data={'ligma': 'balls', 'sugandese': 'nuts'}
            )
        pass
        # POST
        # Найти юзера по токену
        # Установить новый тг айди
        # Передать данные юзера в сериализатор

# При каждом запросе кроме установки токена проверять, что юзер с текущим тг чат айди есть в БД
#