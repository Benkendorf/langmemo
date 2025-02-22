import pytest
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

from deck.forms import DeckForm
from deck.models import Card


def test_deck_is_on_homepage(deck_owner_client, cards):
    """Проверка, что информация о колоде выводится на главную."""

    response = deck_owner_client.get(reverse('homepage:index'))
    print(response.context['object_list'][0].cards_in_queue)
    page_obj = response.context['object_list']
    deck_count = page_obj.count()
    card_count = page_obj[0].card_count
    winrate = page_obj[0].winrate
    cards_in_queue = page_obj[0].cards_in_queue
    assert deck_count == 1
    assert card_count == len(cards)
    assert winrate == sum(card.winrate for card in cards)/len(cards)
    assert cards_in_queue == Card.objects.filter(
        deck=page_obj[0],
        in_queue=True
    ).count()


@pytest.mark.parametrize(
    'parametrized_client',
    (
        pytest.lazy_fixture('client'),
        pytest.lazy_fixture('not_deck_owner_client'),
    )
)
def test_deck_is_not_on_other_user_or_anon_homepage(parametrized_client,
                                                    cards):
    """Проверка, что информация о колоде не выводится другому пользователю."""

    response = parametrized_client.get(reverse('homepage:index'))
    assert len(response.context['object_list']) == 0


def test_homepage_contains_form(deck_owner_client):
    """Проверка, что на главной есть форма создания колоды."""

    url = reverse('homepage:index')
    response = deck_owner_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], DeckForm)


def test_calendar(deck_owner, deck_owner_client, cards_for_calendar):
    """Проверка корректности информации, выводимой в календаре ревью."""

    url = reverse('homepage:index')
    response = deck_owner_client.get(url)
    assert response.context['cards_total_now'] == Card.objects.filter(
        deck__user=deck_owner,
        in_queue=True
    ).count()
    assert response.context['calendar'][1]['end_of_day'] == 2


def test_password_change_contains_form(deck_owner_client):
    """Проверка, что на странице смены пароля есть соответствующая форма."""

    url = reverse('password_change')
    response = deck_owner_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], PasswordChangeForm)
