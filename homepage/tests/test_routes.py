import pytest

from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_deck_owner_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('deck_owner_client'), HTTPStatus.OK)
    )
)
def test_index_page_availability(parametrized_client, expected_status):
    url = reverse('homepage:index')
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('homepage:create_deck', None),
        ('homepage:delete_deck', pytest.lazy_fixture('deck_id_for_args'))
    )
)
def test_create_and_delete_deck_redirect_for_anon(name, args, client):
    url = reverse(name, args=args)
    response = client.get(url)
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_deck_owner_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('deck_owner_client'), HTTPStatus.OK)
    )
)
def test_create_deck_availability(parametrized_client, expected_status):
    url = reverse('homepage:create_deck')
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_deck_owner_client'), HTTPStatus.FORBIDDEN),
        (pytest.lazy_fixture('deck_owner_client'), HTTPStatus.OK)
    )
)
def test_delete_deck_availability(parametrized_client, expected_status,
                                  deck_id_for_args):
    url = reverse('homepage:delete_deck', args=deck_id_for_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


def test_user_change_password_availability(deck_owner_client):
    url = reverse('password_change')
    response = deck_owner_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_anon_change_password_redirect(client):
    url = reverse('password_change')
    response = client.get(url)
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, expected_url)
