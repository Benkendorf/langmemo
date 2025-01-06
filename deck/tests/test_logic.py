# Здесь протестировать:

# Добавление карты +
# Удаление карты +
# Обновление инфы в карте после ревью
# Проверить, что работают все три варианта ответа
# Проверка работы Дам-Лев
# Обновление статуса in_queue
#
# Анон не может ничего делать

from datetime import timedelta
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertRedirects
from deck.models import Card
from deck.views import (SRS_LEVELS,
                        REVIEW_SUCCESS_MESSAGE,
                        REVIEW_FAILURE_MESSAGE,
                        REVIEW_NOT_IN_QUEUE_MESSAGE)


@pytest.mark.parametrize(
    'data',
    (
        pytest.lazy_fixture('data_for_card'),
        pytest.lazy_fixture('no_answers_data_for_card'),
    ),
)
def test_anon_cant_create_card(client, deck_id_for_args, data):
    url = reverse('deck:create_card', args=deck_id_for_args)
    client.post(url, data=data)
    card_count = Card.objects.count()
    assert card_count == 0


@pytest.mark.parametrize(
    'data',
    (
        pytest.lazy_fixture('data_for_card'),
        pytest.lazy_fixture('no_answers_data_for_card'),
    ),
)
def test_not_deck_owner_cant_create_card(not_deck_owner_client,
                                         deck_id_for_args, data):
    url = reverse('deck:create_card', args=deck_id_for_args)
    response = not_deck_owner_client.post(url, data=data)
    card_count = Card.objects.count()
    assert card_count == 0
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_deck_owner_can_create_card_with_correct_data(
        deck_owner_client,
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


def test_deck_owner_cant_create_card_with_incorrect_data(
        deck_owner_client,
        deck_id_for_args,
        no_answers_data_for_card):

    url = reverse('deck:create_card', args=deck_id_for_args)
    deck_owner_client.post(url, data=no_answers_data_for_card)
    card_count = Card.objects.count()
    assert card_count == 0


def test_deck_owner_can_delete_card(
        deck_owner_client,
        deck_id_for_args,
        cards,
        card_not_in_queue_id_for_args):

    url = reverse('deck:delete_card', args=card_not_in_queue_id_for_args)
    response = deck_owner_client.post(url)
    card_count = Card.objects.count()
    assert card_count == len(cards) - 1
    assert not Card.objects.filter(
        id=card_not_in_queue_id_for_args[0]
    ).exists()
    assertRedirects(response, reverse('deck:card_list', args=deck_id_for_args))


def test_anon_cant_delete_card(
        client,
        cards,
        card_not_in_queue_id_for_args):
    url = reverse('deck:delete_card', args=card_not_in_queue_id_for_args)
    client.post(url)
    card_count = Card.objects.count()
    assert card_count == len(cards)


def test_not_deck_owner_cant_delete_card(
        not_deck_owner_client,
        cards,
        card_not_in_queue_id_for_args):
    url = reverse('deck:delete_card', args=card_not_in_queue_id_for_args)
    not_deck_owner_client.post(url)
    card_count = Card.objects.count()
    assert card_count == len(cards)


@pytest.mark.parametrize(
    'card, card_id, response_message',
    (
        (pytest.lazy_fixture('rev_card_0'), 1, REVIEW_NOT_IN_QUEUE_MESSAGE),
        (pytest.lazy_fixture('rev_card_1'), 2, REVIEW_SUCCESS_MESSAGE)
    ),
)
def test_reviewed_card_info_updates(deck_owner_client,
                                    cards_for_review_testing,
                                    card, card_id, response_message):
    url = reverse('deck:review_check', args=(card_id,))
    response = deck_owner_client.post(
        url,
        data={
            'answer': card.answer_1
        }
    )
    print(card)
    print(card.id)
    assert card == cards_for_review_testing[card_id - 1]
    assert response.context['message'] == response_message
