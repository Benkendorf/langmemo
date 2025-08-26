# Здесь протестировать:

# Добавление карты +
# Удаление карты +
# Обновление инфы в карте после успешного ревью +
# Обновление инфы в карте после проваленного ревью +
# Проверить, что работают все три варианта ответа +
# Проверка работы Дам-Лев +
# Проверка refresh_queue (в т.ч. что при ревью обновляется только текущая колода) +
#
# Анон не может ничего делать

from datetime import timedelta
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertRedirects
from deck.models import Card
from deck.views import (REVIEW_SUCCESS_MESSAGE,
                        REVIEW_NOT_PERFECT_SUCCESS_MESSAGE,
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
    """Проверка, что аноним не может создать карту."""
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
    """Проверка, что пользователь не может создать карту в чужой колоде."""
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
    """Проверка, что пользователь может создать карту в своей колоде."""

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
    """Проверка, что пользователь не может создать карту без единого ответа."""

    url = reverse('deck:create_card', args=deck_id_for_args)
    deck_owner_client.post(url, data=no_answers_data_for_card)
    card_count = Card.objects.count()
    assert card_count == 0


def test_deck_owner_can_delete_card(
        deck_owner_client,
        deck_id_for_args,
        cards,
        card_not_in_queue_id_for_args):
    """Проверка, что пользователь может удалить карту в своей колоде."""

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
    """Проверка, что аноним не может удалить карту."""

    url = reverse('deck:delete_card', args=card_not_in_queue_id_for_args)
    client.post(url)
    card_count = Card.objects.count()
    assert card_count == len(cards)


def test_not_deck_owner_cant_delete_card(
        not_deck_owner_client,
        cards,
        card_not_in_queue_id_for_args):
    """Проверка, что пользователь не может удалить карту в чужой колоде."""

    url = reverse('deck:delete_card', args=card_not_in_queue_id_for_args)
    not_deck_owner_client.post(url)
    card_count = Card.objects.count()
    assert card_count == len(cards)


def test_anon_cant_edit_card(
        client,
        cards,
        data_for_card_editing):
    """Проверка, что аноним не может редактировать карту."""

    initial_question = cards[0].question
    initial_answer_1 = cards[0].answer_1
    initial_answer_2 = cards[0].answer_2
    initial_answer_3 = cards[0].answer_3

    url = reverse('deck:edit_card', args=(cards[0].id,))
    client.post(url, data=data_for_card_editing)

    cards[0].refresh_from_db()

    assert cards[0].question == initial_question
    assert cards[0].answer_1 == initial_answer_1
    assert cards[0].answer_2 == initial_answer_2
    assert cards[0].answer_3 == initial_answer_3


def test_not_deck_owner_cant_edit_card(
        not_deck_owner_client,
        cards,
        data_for_card_editing):
    """Проверка, что пользователь не может
    редактировать карту в чужой колоде.
    """

    initial_question = cards[0].question
    initial_answer_1 = cards[0].answer_1
    initial_answer_2 = cards[0].answer_2
    initial_answer_3 = cards[0].answer_3

    url = reverse('deck:edit_card', args=(cards[0].id,))
    not_deck_owner_client.post(url, data=data_for_card_editing)

    cards[0].refresh_from_db()

    assert cards[0].question == initial_question
    assert cards[0].answer_1 == initial_answer_1
    assert cards[0].answer_2 == initial_answer_2
    assert cards[0].answer_3 == initial_answer_3


def test_deck_owner_cant_edit_card_with_incomplete_data(
        not_deck_owner_client,
        cards,
        no_answers_data_for_card):
    """Проверка, что пользователь не может при редактировании
    оставить у карты ноль ответов.
    """

    initial_question = cards[0].question
    initial_answer_1 = cards[0].answer_1
    initial_answer_2 = cards[0].answer_2
    initial_answer_3 = cards[0].answer_3

    url = reverse('deck:edit_card', args=(cards[0].id,))
    not_deck_owner_client.post(url, data=no_answers_data_for_card)

    cards[0].refresh_from_db()

    assert cards[0].question == initial_question
    assert cards[0].answer_1 == initial_answer_1
    assert cards[0].answer_2 == initial_answer_2
    assert cards[0].answer_3 == initial_answer_3


def test_deck_owner_can_edit_card(
        deck_owner_client,
        cards,
        data_for_card_editing):
    """Проверка, что пользователь может редактировать карту."""
    url = reverse('deck:edit_card', args=(cards[0].id,))
    deck_owner_client.post(url, data=data_for_card_editing)

    cards[0].refresh_from_db()

    assert cards[0].question == data_for_card_editing['question']
    assert cards[0].answer_1 == data_for_card_editing['answer_1']
    assert cards[0].answer_2 == data_for_card_editing['answer_2']
    assert cards[0].answer_3 == data_for_card_editing['answer_3']


@pytest.mark.parametrize(
    ('card, card_id, response_message, plus_right_answers, new_srs_xp,'
     'new_srs_level'),
    (
        (pytest.lazy_fixture('rev_card_0'),
         pytest.lazy_fixture('rev_card_0_id_for_args'),
         REVIEW_NOT_IN_QUEUE_MESSAGE,
         0,
         0,
         0),

        (pytest.lazy_fixture('rev_card_1'),
         pytest.lazy_fixture('rev_card_1_id_for_args'),
         REVIEW_SUCCESS_MESSAGE,
         1,
         1,
         0),

        (pytest.lazy_fixture('rev_card_2'),
         pytest.lazy_fixture('rev_card_2_id_for_args'),
         REVIEW_SUCCESS_MESSAGE,
         1,
         0,
         1),

        (pytest.lazy_fixture('rev_card_3'),
         pytest.lazy_fixture('rev_card_3_id_for_args'),
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
    """Проверка обновления информации в успешно отревьюенной карте."""

    initial_right_guesses = card.right_guesses
    initial_wrong_guesses = card.wrong_guesses
    url = reverse('deck:review_check', args=card_id)
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
    try:
        assert card.winrate == (100 * card.right_guesses
                                / (card.right_guesses + card.wrong_guesses))
    except ZeroDivisionError:
        assert card.winrate is None
    assert card.srs_xp == new_srs_xp
    assert card.srs_level == new_srs_level
    assert card.in_queue is False
    assert card.datetime_reviewed - timezone.now() < timedelta(seconds=1)



@pytest.mark.parametrize(
    ('card, card_id, response_message, plus_wrong_answers, new_srs_xp,'
     'new_srs_level'),
    (
        (pytest.lazy_fixture('rev_card_0'),
         pytest.lazy_fixture('rev_card_0_id_for_args'),
         REVIEW_NOT_IN_QUEUE_MESSAGE,
         0,
         0,
         0),

        (pytest.lazy_fixture('rev_card_1'),
         pytest.lazy_fixture('rev_card_1_id_for_args'),
         REVIEW_FAILURE_MESSAGE,
         1,
         0,
         0),

        (pytest.lazy_fixture('rev_card_2'),
         pytest.lazy_fixture('rev_card_2_id_for_args'),
         REVIEW_FAILURE_MESSAGE,
         1,
         0,
         0),

        (pytest.lazy_fixture('rev_card_3'),
         pytest.lazy_fixture('rev_card_3_id_for_args'),
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
    """Проверка обновления информации в неуспешно отревьюенной карте."""

    initial_right_guesses = card.right_guesses
    initial_wrong_guesses = card.wrong_guesses
    url = reverse('deck:review_check', args=card_id)
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
    try:
        assert card.winrate == (100 * card.right_guesses
                                / (card.right_guesses + card.wrong_guesses))
    except ZeroDivisionError:
        assert card.winrate is None
    assert card.srs_xp == new_srs_xp
    assert card.srs_level == new_srs_level
    assert card.in_queue is False
    assert card.datetime_reviewed - timezone.now() < timedelta(seconds=1)


def test_anon_cant_review_card(client, rev_card_1):
    """Проверка, что аноним не может сделать ревью карты."""

    initial_right_guesses = rev_card_1.right_guesses
    initial_wrong_guesses = rev_card_1.wrong_guesses
    initial_srs_xp = rev_card_1.srs_xp
    initial_srs_level = rev_card_1.srs_level
    initial_datetime_reviewed = rev_card_1.datetime_reviewed

    url = reverse('deck:review_check', args=(rev_card_1.id,))
    redirect_url = reverse('login') + '?next=' + url
    response = client.post(
        url,
        data={
            'answer': 'some_answer',
        }
    )
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, redirect_url)

    rev_card_1.refresh_from_db()
    assert rev_card_1.right_guesses == initial_right_guesses
    assert rev_card_1.wrong_guesses == initial_wrong_guesses
    assert rev_card_1.srs_xp == initial_srs_xp
    assert rev_card_1.srs_level == initial_srs_level
    assert rev_card_1.in_queue is True
    assert rev_card_1.datetime_reviewed == initial_datetime_reviewed


@pytest.mark.parametrize(
    'answer',
    (
        pytest.lazy_fixture('rev_card_1_ans_1'),
        pytest.lazy_fixture('rev_card_1_ans_2'),
        pytest.lazy_fixture('rev_card_1_ans_3')
    )
)
def test_all_answers_work(deck_owner_client, rev_card_1, answer):
    """Проверка, что каждый из трех ответов работает в ревью."""

    initial_right_guesses = rev_card_1.right_guesses
    initial_wrong_guesses = rev_card_1.wrong_guesses
    initial_srs_xp = rev_card_1.srs_xp
    initial_srs_level = rev_card_1.srs_level

    url = reverse('deck:review_check', args=(rev_card_1.id,))
    response = deck_owner_client.post(
        url,
        data={
            'answer': answer,
        }
    )

    assert response.context['message'] == REVIEW_SUCCESS_MESSAGE
    rev_card_1.refresh_from_db()
    assert rev_card_1.right_guesses == initial_right_guesses + 1
    assert rev_card_1.wrong_guesses == initial_wrong_guesses
    try:
        assert rev_card_1.winrate == (100 * rev_card_1.right_guesses
                                      / (rev_card_1.right_guesses
                                         + rev_card_1.wrong_guesses))
    except ZeroDivisionError:
        assert rev_card_1.winrate is None
    assert rev_card_1.srs_xp == initial_srs_xp + 1
    assert rev_card_1.srs_level == initial_srs_level
    assert rev_card_1.in_queue is False
    assert rev_card_1.datetime_reviewed - timezone.now() < timedelta(seconds=1)


@pytest.mark.parametrize(
    'answer',
    (
        ['second_rev_answer_1'[:n] + 'x' + 'second_rev_answer_1'[n:] for n in range(len('second_rev_answer_1') + 1)]   # insertion
        + ['second_rev_answer_1'[:n - 1] + 'x' + 'second_rev_answer_1'[n:] for n in range(1, len('second_rev_answer_1') + 1)]  # substitution
        + ['second_rev_answer_1'[:n - 1] + 'second_rev_answer_1'[n:] for n in range(1, len('second_rev_answer_1') + 1)]   # deletion
        + ['second_rev_answer_1'[:n] + 'second_rev_answer_1'[n + 1] + 'second_rev_answer_1'[n] + 'second_rev_answer_1'[n + 2:] for n in range(0, len('second_rev_answer_1') - 1)]    # Damerau transposition
    )
)
def test_levenshtein_variants(deck_owner_client, rev_card_1, answer):
    """Проверка, что любая строка с расстоянием
    Дамерау-Левенштейна = 1 от правильной, подходит в ревью.
    """

    initial_right_guesses = rev_card_1.right_guesses
    initial_wrong_guesses = rev_card_1.wrong_guesses
    initial_srs_xp = rev_card_1.srs_xp
    initial_srs_level = rev_card_1.srs_level

    url = reverse('deck:review_check', args=(rev_card_1.id,))
    response = deck_owner_client.post(
        url,
        data={
            'answer': answer,
        }
    )
    assert response.context['message'] == REVIEW_NOT_PERFECT_SUCCESS_MESSAGE
    rev_card_1.refresh_from_db()
    assert rev_card_1.right_guesses == initial_right_guesses + 1
    assert rev_card_1.wrong_guesses == initial_wrong_guesses
    try:
        assert rev_card_1.winrate == (100 * rev_card_1.right_guesses
                                      / (rev_card_1.right_guesses
                                         + rev_card_1.wrong_guesses))
    except ZeroDivisionError:
        assert rev_card_1.winrate is None
    assert rev_card_1.srs_xp == initial_srs_xp + 1
    assert rev_card_1.srs_level == initial_srs_level
    assert rev_card_1.in_queue is False
    assert rev_card_1.datetime_reviewed - timezone.now() < timedelta(seconds=1)


@pytest.mark.parametrize(
    'name',
    (
        'deck:card_list',
        'deck:review_display'
    )
)
def test_refresh_queue_for_current_deck_cases(name, refresh_queue_card_0,
                                              refresh_queue_card_1,
                                              deck_owner_client):
    """Проверяем обновление очереди в представлениях,
    в которых обновляется только текущая колода.
    """

    url = reverse(name, args=(refresh_queue_card_0.deck.id,))
    deck_owner_client.get(url)

    refresh_queue_card_0.refresh_from_db()
    refresh_queue_card_1.refresh_from_db()
    assert refresh_queue_card_0.in_queue is True
    assert refresh_queue_card_1.in_queue is False


@pytest.mark.parametrize(
    'data',
    (
        pytest.lazy_fixture('data_for_card'),
        pytest.lazy_fixture('no_answers_data_for_card'),
    )
)
def test_refresh_queue_for_create_card(data, refresh_queue_card_0,
                                       refresh_queue_card_1,
                                       deck_owner_client):
    """Отдельный тест для представления создания карты,
    т.к. здесь применяется метод POST.
    """

    url = reverse('deck:create_card', args=(refresh_queue_card_0.deck.id,))
    deck_owner_client.post(
        url,
        data=data
    )

    refresh_queue_card_0.refresh_from_db()
    refresh_queue_card_1.refresh_from_db()
    assert refresh_queue_card_0.in_queue is True
    assert refresh_queue_card_1.in_queue is False


def test_refresh_queue_for_homepage(refresh_queue_card_0,
                                    refresh_queue_card_1,
                                    deck_owner_client):
    """Проверка, что на главной странице обновляются все колоды."""

    url = reverse('homepage:index')
    deck_owner_client.get(url)

    refresh_queue_card_0.refresh_from_db()
    refresh_queue_card_1.refresh_from_db()
    assert refresh_queue_card_0.in_queue is True
    assert refresh_queue_card_1.in_queue is True
