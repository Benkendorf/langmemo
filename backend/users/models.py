from django.contrib.auth.models import AbstractUser
from django.db import models

from django_mem_cards.constants import API_TOKEN_LENGTH, TG_USER_ID_MAX_LENGTH


class CustomUser(AbstractUser):
    email = models.EmailField(('Адрес электронной почты'))  # Переопределяем без blank=True, чтобы имейл был обязательным
    api_token = models.CharField(
        max_length=API_TOKEN_LENGTH,
        unique=True,
        null=True,
        blank=True
    )
    telegram_chat_id = models.CharField(max_length=TG_USER_ID_MAX_LENGTH, null=True, blank=True, unique=True)
