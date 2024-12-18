import pytest

from django.contrib.auth.hashers import make_password
from django.test.client import Client


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def deck_owner(django_user_model):
    return django_user_model.objects.create(
        username='deck_owner',
        password=make_password('zwerty789')
    )


@pytest.fixture
def not_deck_owner(django_user_model):
    return django_user_model.objects.create(username='some_guy')


@pytest.fixture
def deck_owner_client(deck_owner):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(deck_owner)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_deck_owner_client(not_deck_owner):
    client = Client()
    client.force_login(not_deck_owner)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def registration_data():
    return {'username': 'test_user',
            'password1': 'zwerty789',
            'password2': 'zwerty789'}   # Поле Confirm Password


@pytest.fixture
def login_data(registration_data):
    return {'username': registration_data['username'],
            'password': registration_data['password1']}


@pytest.fixture
def password_change_data():
    return {'old_password': 'zwerty789',
            'new_password1': 'new_zwerty789',
            'new_password2': 'new_zwerty789'}   # Поле Confirm Password
