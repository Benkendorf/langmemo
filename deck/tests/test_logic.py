# Здесь протестировать:

# Добавление карты
# Удаление карты
# Обновление инфы в карте после ревью
# Обновление статуса in_queue
#
# Анон не может ничего делать

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertRedirects
from deck.models import Card

@pytest.mark.django_db
def test_anonymous_user_cant_create_card(client, deck_id_for_args,
                                         data_for_card):
    url = reverse('deck:create_card', args=deck_id_for_args)
    client.post(url, data=data_for_card)
    card_count = Card.objects.count()
    assert card_count == 0


def test_user_can_create_card_with_correct_data(deck_owner_client,
                                                deck,
                                                deck_id_for_args,
                                                data_for_card):
    url = reverse('deck:create_card', args=deck_id_for_args)
    response = deck_owner_client.post(url, data=data_for_card)

    rough_dt_created = timezone.now()

    assertRedirects(response, reverse('deck:card_list', args=deck_id_for_args))
    card_count = Card.objects.count()
    assert card_count == 1
    card = Card.objects.get()
    assert card.deck == deck
    assert card.question == data_for_card['question']
    assert card.answer_1 == data_for_card['answer_1']
    assert card.answer_2 == data_for_card['answer_2']
    assert card.answer_3 == data_for_card['answer_3']
    assert card.right_guesses == 0
    assert card.wrong_guesses == 0
    assert card.winrate is None
    assert card.datetime_reviewed is None
    assert card.datetime_created - rough_dt_created < timedelta(seconds=1)
