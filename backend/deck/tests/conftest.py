import pytest

from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.test.client import Client
from django.utils import timezone

from deck.models import Card, Deck


@pytest.fixture
def deck_owner(django_user_model):
    return django_user_model.objects.create(
        username='deck_owner',
        password=make_password('zwerty789')
    )


@pytest.fixture
def not_deck_owner(django_user_model):
    return django_user_model.objects.create(username='not_owner')


@pytest.fixture
def deck_owner_client(deck_owner):
    client = Client()
    client.force_login(deck_owner)
    return client


@pytest.fixture
def not_deck_owner_client(not_deck_owner):
    client = Client()
    client.force_login(not_deck_owner)
    return client


@pytest.fixture
def deck(deck_owner):
    return Deck.objects.create(
        user=deck_owner,
        deck_name='test_deck'
    )


@pytest.fixture
def data_for_deck():
    return {
        'deck_name': 'test_deck'
    }


@pytest.fixture
def data_for_card():
    return {
        'question': 'added_question',
        'answer_1': 'added_answer_1',
        'answer_2': 'added_answer_2',
        'answer_3': 'added_answer_3',
    }


@pytest.fixture
def no_answers_data_for_card():
    return {
        'question': 'added_question',
        'answer_1': '',
        'answer_2': '',
        'answer_3': '',
    }


@pytest.fixture
def data_for_card_editing():
    return {
        'question': 'edited_question',
        'answer_1': 'edited_answer_1',
        'answer_2': 'edited_answer_2',
        'answer_3': 'edited_answer_3',
    }


@pytest.fixture
def deck_id_for_args(deck):
    return (deck.id, )


@pytest.fixture
def cards(deck):
    all_cards = [
        Card.objects.create(
            deck=deck,
            question='first_test_question',
            answer_1='first_test_answer_1',
            answer_2='first_test_answer_2',
            answer_3='first_test_answer_3',
            right_guesses=3,
            wrong_guesses=1,
            datetime_created=timezone.now() - timedelta(days=20),
            datetime_reviewed=timezone.now() - timedelta(hours=1),
            srs_level=0,
            srs_xp=0
        ),
        Card.objects.create(
            deck=deck,
            question='second_test_question',
            answer_1='second_test_answer_1',
            answer_2='second_test_answer_2',
            answer_3='second_test_answer_3',
            right_guesses=1,
            wrong_guesses=2,
            datetime_created=timezone.now() - timedelta(days=15),
            datetime_reviewed=timezone.now() - timedelta(hours=6, minutes=1),
            srs_level=0,
            srs_xp=0
        )
    ]
    return all_cards


@pytest.fixture
def card_not_in_queue_id_for_args(cards):
    return (cards[0].id, )


@pytest.fixture
def card_in_queue_id_for_args(cards):
    return (cards[1].id, )


@pytest.fixture
def cards_for_review_testing(deck):
    all_cards = [
        Card.objects.create(                           # NOT IN QUEUE
            deck=deck,
            question='first_rev_question',
            answer_1='first_rev_answer_1',
            answer_2='first_rev_answer_2',
            answer_3='first_rev_answer_3',
            right_guesses=0,
            wrong_guesses=0,
            datetime_created=timezone.now() - timedelta(days=20),
            datetime_reviewed=timezone.now() - timedelta(hours=1),
            srs_level=0,
            srs_xp=0,
            in_queue=False
        ),
        Card.objects.create(                           # IN QUEUE
            deck=deck,
            question='second_rev_question',
            answer_1='second_rev_answer_1',
            answer_2='second_rev_answer_2',
            answer_3='second_rev_answer_3',
            right_guesses=0,
            wrong_guesses=0,
            datetime_created=timezone.now() - timedelta(days=15),
            srs_level=0,
            srs_xp=0
        ),
        Card.objects.create(                           # IN QUEUE
            deck=deck,
            question='third_rev_question',
            answer_1='third_rev_answer_1',
            answer_2='third_rev_answer_2',
            answer_3='third_rev_answer_3',
            right_guesses=0,
            wrong_guesses=0,
            datetime_created=timezone.now() - timedelta(days=15),
            srs_level=0,
            srs_xp=2            # После правильного ответа - плюс уровень
        ),
        Card.objects.create(                           # IN QUEUE
            deck=deck,
            question='fourth_rev_question',
            answer_1='fourth_rev_answer_1',
            answer_2='fourth_rev_answer_2',
            answer_3='fourth_rev_answer_3',
            right_guesses=0,
            wrong_guesses=0,
            datetime_created=timezone.now() - timedelta(days=15),
            srs_level=4,
            srs_xp=0        # На максимальном 4м уровне опыт не прибавляется
        )

    ]
    return all_cards


@pytest.fixture
def rev_card_0(cards_for_review_testing):
    return cards_for_review_testing[0]


@pytest.fixture
def rev_card_1(cards_for_review_testing):
    return cards_for_review_testing[1]


@pytest.fixture
def rev_card_2(cards_for_review_testing):
    return cards_for_review_testing[2]


@pytest.fixture
def rev_card_3(cards_for_review_testing):
    return cards_for_review_testing[3]


@pytest.fixture
def rev_card_0_id_for_args(rev_card_0):
    return (rev_card_0.id, )


@pytest.fixture
def rev_card_1_id_for_args(rev_card_1):
    return (rev_card_1.id, )


@pytest.fixture
def rev_card_2_id_for_args(rev_card_2):
    return (rev_card_2.id, )


@pytest.fixture
def rev_card_3_id_for_args(rev_card_3):
    return (rev_card_3.id, )


@pytest.fixture
def rev_card_1_ans_1(rev_card_1):
    return rev_card_1.answer_1


@pytest.fixture
def rev_card_1_ans_2(rev_card_1):
    return rev_card_1.answer_2


@pytest.fixture
def rev_card_1_ans_3(rev_card_1):
    return rev_card_1.answer_3


@pytest.fixture
def rev_card_1_levenshtein(rev_card_1_ans_1):
    return [[rev_card_1_ans_1[:n] + 'x' + rev_card_1_ans_1[n:] for n in range(len(rev_card_1_ans_1) + 1)]
            + [rev_card_1_ans_1[:n - 1] + 'x' + rev_card_1_ans_1[n:] for n in range(1, len(rev_card_1_ans_1) + 1)]
            + [rev_card_1_ans_1[:n - 1] + rev_card_1_ans_1[n:] for n in range(1, len(rev_card_1_ans_1) + 1)]]


@pytest.fixture
def deck_for_refresh_queue_1(deck_owner):
    return Deck.objects.create(
        user=deck_owner,
        deck_name='deck_for_refresh_queue_1'
    )


@pytest.fixture
def deck_for_refresh_queue_2(deck_owner):
    return Deck.objects.create(
        user=deck_owner,
        deck_name='deck_for_refresh_queue_2'
    )


@pytest.fixture
def cards_for_refresh_queue(deck_for_refresh_queue_1,
                            deck_for_refresh_queue_2):
    all_cards = [
        Card.objects.create(
            deck=deck_for_refresh_queue_1,
            question='first_test_question',
            answer_1='first_test_answer_1',
            answer_2='first_test_answer_2',
            answer_3='first_test_answer_3',
            datetime_created=timezone.now() - timedelta(days=20),
            in_queue=False
        ),
        Card.objects.create(
            deck=deck_for_refresh_queue_2,
            question='second_test_question',
            answer_1='second_test_answer_1',
            answer_2='second_test_answer_2',
            answer_3='second_test_answer_3',
            datetime_created=timezone.now() - timedelta(days=15),
            in_queue=False
        )
    ]
    return all_cards


@pytest.fixture
def refresh_queue_card_0(cards_for_refresh_queue):
    return cards_for_refresh_queue[0]


@pytest.fixture
def refresh_queue_card_1(cards_for_refresh_queue):
    return cards_for_refresh_queue[1]
