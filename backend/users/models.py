from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(('Адрес электронной почты'))  # Переопределяем без blank=True, чтобы имейл был обязательным
