# Здесь протестировать:

# Добавление карты +
# Удаление карты +
# Обновление инфы в карте после успешного ревью +
# Обновление инфы в карте после проваленного ревью +
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
    assert card.datetime_created - timezone.now() < timedelta(seconds=1)


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
    ('card, card_id, response_message, plus_right_answers, new_srs_xp,'
     'new_srs_level'),
    (
        (pytest.lazy_fixture('rev_card_0'),
         1,
         REVIEW_NOT_IN_QUEUE_MESSAGE,
         0,
         0,
         0),

        (pytest.lazy_fixture('rev_card_1'),
         2,
         REVIEW_SUCCESS_MESSAGE,
         1,
         1,
         0),

        (pytest.lazy_fixture('rev_card_2'),
         3,
         REVIEW_SUCCESS_MESSAGE,
         1,
         0,
         1),

        (pytest.lazy_fixture('rev_card_3'),
         4,
         REVIEW_SUCCESS_MESSAGE,
         1,
         0,
         4)
    ),
)
def test_succesfully_reviewed_card_updates(deck_owner_client,
                                           card, card_id, response_message,
                                           plus_right_answers, new_srs_xp,
                                           new_srs_level):
    initial_right_guesses = card.right_guesses
    initial_wrong_guesses = card.wrong_guesses
    url = reverse('deck:review_check', args=(card_id,))
    response = deck_owner_client.post(
        url,
        data={
            'answer': card.answer_1,
        }
    )
    assert response.context['message'] == response_message
    card.refresh_from_db()
    assert card.right_guesses == initial_right_guesses + plus_right_answers
    assert card.wrong_guesses == initial_wrong_guesses
    assert card.srs_xp == new_srs_xp
    assert card.srs_level == new_srs_level
    assert card.in_queue is False
    assert card.datetime_reviewed - timezone.now() < timedelta(seconds=1)



@pytest.mark.parametrize(
    ('card, card_id, response_message, plus_wrong_answers, new_srs_xp,'
     'new_srs_level'),
    (
        (pytest.lazy_fixture('rev_card_0'),
         1,
         REVIEW_NOT_IN_QUEUE_MESSAGE,
         0,
         0,
         0),

        (pytest.lazy_fixture('rev_card_1'),
         2,
         REVIEW_FAILURE_MESSAGE,
         1,
         0,
         0),

        (pytest.lazy_fixture('rev_card_2'),
         3,
         REVIEW_FAILURE_MESSAGE,
         1,
         0,
         0),

        (pytest.lazy_fixture('rev_card_3'),
         4,
         REVIEW_FAILURE_MESSAGE,
         1,
         0,
         3)
    ),
)
def test_unsuccesfully_reviewed_card_updates(deck_owner_client,
                                             card, card_id, response_message,
                                             plus_wrong_answers, new_srs_xp,
                                             new_srs_level):
    initial_right_guesses = card.right_guesses
    initial_wrong_guesses = card.wrong_guesses
    url = reverse('deck:review_check', args=(card_id,))
    response = deck_owner_client.post(
        url,
        data={
            'answer': 'wrong',
        }
    )
    assert response.context['message'] == response_message
    card.refresh_from_db()
    assert card.right_guesses == initial_right_guesses
    assert card.wrong_guesses == initial_wrong_guesses + plus_wrong_answers
    assert card.srs_xp == new_srs_xp
    assert card.srs_level == new_srs_level
    assert card.in_queue is False
    assert card.datetime_reviewed - timezone.now() < timedelta(seconds=1)
