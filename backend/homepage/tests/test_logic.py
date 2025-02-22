# Тут тесты, что колоды удалются (владельцами) и добавляются.
from http import HTTPStatus

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from deck.models import Deck


def test_user_can_create_deck(deck_owner, deck_owner_client, data_for_deck):
    """Проверка, что пользователь может создать новую колоду."""

    response = deck_owner_client.post(
        reverse('homepage:create_deck'),
        data=data_for_deck
    )
    assert Deck.objects.count() == 1
    deck = Deck.objects.get()
    assertRedirects(response, reverse('deck:card_list', args=(deck.id, )))
    assert deck.user == deck_owner
    assert deck.deck_name == data_for_deck['deck_name']


def test_user_can_delete_deck(deck_owner_client, deck):
    """Проверка, что пользователь может удалить свою колоду."""

    response = deck_owner_client.post(
        reverse('homepage:delete_deck', args=(deck.id, ))
    )
    assertRedirects(response, reverse('homepage:index'))
    assert Deck.objects.count() == 0


def test_user_cant_delete_others_deck(not_deck_owner_client, deck_owner, deck,
                                      data_for_deck):
    """Проверка, что пользователь не может удалить чужую колоду."""

    response = not_deck_owner_client.post(
        reverse('homepage:delete_deck', args=(deck.id, ))
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert Deck.objects.count() == 1
    deck = Deck.objects.get()
    assert deck.user == deck_owner
    assert deck.deck_name == data_for_deck['deck_name']


def test_user_can_change_password(deck_owner_client, deck_owner,
                                  password_change_data):
    """Проверка, что пользователь может сменить пароль."""

    url = reverse('password_change')
    response = deck_owner_client.post(url, data=password_change_data)
    assert response.status_code == HTTPStatus.FOUND
    redirect_url = reverse('password_change_done')
    assertRedirects(response, redirect_url)
    deck_owner.refresh_from_db()
    assert check_password(
        password_change_data['new_password1'],
        deck_owner.password
    )


def test_anon_cant_change_password(client, password_change_data):
    """Проверка, что пользователь не может сменить пароль."""

    url = reverse('password_change')
    response = client.post(url, data=password_change_data)
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, expected_url)
