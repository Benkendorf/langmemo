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
def deck_id_for_args(deck):
    return (deck.id, )


@pytest.fixture
def cards(deck):
    all_cards = [
        Card.objects.create(                           # NOT IN QUEUE
            deck=deck,
            question='first_test_question',
            answer_1='first_test_answer_1',
            answer_2='first_test_answer_2',
            answer_3='first_test_answer_3',
            right_guesses=3,
            wrong_guesses=1,
            datetime_created=timezone.now() - timedelta(days=15),
            datetime_reviewed=timezone.now() - timedelta(hours=1),
            srs_level=0,
            srs_xp=0
        ),
        Card.objects.create(                           # IN QUEUE
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
def cards_for_calendar(deck):
    all_cards = [
        Card.objects.create(                           # NOT IN QUEUE
            deck=deck,
            question='first_test_question',
            answer_1='first_test_answer_1',
            answer_2='first_test_answer_2',
            answer_3='first_test_answer_3',
            right_guesses=3,
            wrong_guesses=1,
            datetime_created=timezone.now() - timedelta(days=15),
            datetime_reviewed=timezone.now() - timedelta(hours=1),
            srs_level=0,
            srs_xp=0,
            in_queue=False
        ),
        Card.objects.create(                           # IN QUEUE
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
def password_change_data():
    return {
        'old_password': 'zwerty789',
        'new_password1': 'new_password_789',
        'new_password2': 'new_password_789'
    }


#git test