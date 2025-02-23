from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(('Адрес электронной почты'))  # Переопределяем без blank=True, чтобы имейл был обязательным
    #api_token = models.CharField(
    #    max_length=40,
    #    unique=True,
    #    null=True,
    #    blank=True
    #)
