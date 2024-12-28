# Тут тесты, что на главную выводятся нужные колоды.
import pytest
from django.urls import reverse

from deck.models import Card


def test_deck_is_on_homepage(deck_owner_client, cards):
    response = deck_owner_client.get(reverse('homepage:index'))
    print(response.context['object_list'][0].cards_in_queue)
    page_obj = response.context['object_list']
    deck_count = page_obj.count()
    card_count = page_obj[0].card_count
    winrate = page_obj[0].winrate
    cards_in_queue = page_obj[0].cards_in_queue
    assert deck_count == 1
    assert card_count == 2
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
    response = parametrized_client.get(reverse('homepage:index'))
    assert len(response.context['object_list']) == 0
