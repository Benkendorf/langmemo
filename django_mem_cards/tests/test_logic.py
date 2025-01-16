from datetime import timedelta
from http import HTTPStatus

import pytest

from pytest_django.asserts import assertRedirects

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


@pytest.mark.django_db
def test_anon_can_signup(client, registration_data):
    """Проверка, что аноним может зарегистрироваться."""

    url = reverse('registration')
    redirect_url = reverse('homepage:index')
    response = client.post(url, data=registration_data)
    assertRedirects(response, redirect_url)
    assert CustomUser.objects.count() == 1
    user = CustomUser.objects.get()
    assert check_password(registration_data['password1'], user.password)
    assert user.username == registration_data['username']
    # Проверяем авто-логин
    assert timezone.now() - user.last_login < timedelta(seconds=1)


def test_user_can_login(deck_owner, client, login_data):
    """Проверка, что аноним может залогиниться."""

    url = reverse('login')
    redirect_url = reverse('homepage:index')
    response = client.post(url, data=login_data)
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, redirect_url)
    deck_owner.refresh_from_db()
    assert timezone.now() - deck_owner.last_login < timedelta(seconds=1)


def test_user_can_change_password(deck_owner, deck_owner_client,
                                  password_change_data):
    """Проверка, что пользователь может сменить пароль."""

    url = reverse('password_change')
    redirect_url = reverse('password_change_done')
    response = deck_owner_client.post(url, data=password_change_data)
    assertRedirects(response, redirect_url)
    deck_owner.refresh_from_db()
    assert check_password(
        password_change_data['new_password1'],
        deck_owner.password
    )
