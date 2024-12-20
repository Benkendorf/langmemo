import pytest

from django.contrib.auth.hashers import make_password
from django.test.client import Client

from deck.models import Deck


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
def deck_id_for_args(deck):
    return (deck.id, )
