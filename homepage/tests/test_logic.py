# Тут тесты, что колоды удалются (владельцами) и добавляются.
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from deck.models import Deck


def test_user_can_create_deck(deck_owner, deck_owner_client, data_for_deck):
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
    response = deck_owner_client.post(
        reverse('homepage:delete_deck', args=(deck.id, ))
    )
    assertRedirects(response, reverse('homepage:index'))
    assert Deck.objects.count() == 0


def test_user_cant_delete_others_deck(not_deck_owner_client, deck_owner, deck,
                                      data_for_deck):
    response = not_deck_owner_client.post(
        reverse('homepage:delete_deck', args=(deck.id, ))
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert Deck.objects.count() == 1
    deck = Deck.objects.get()
    assert deck.user == deck_owner
    assert deck.deck_name == data_for_deck['deck_name']
