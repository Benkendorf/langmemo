# Проверяем что получает клиент при GET-запросе
# review_check проверяем в test_logic, т.к. там не разрешен GET.

import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args, expected_status',
    (
        ('deck:card_list',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.OK),

        ('deck:delete_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.OK),

        ('deck:edit_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.OK),

        ('deck:review_display',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.OK),
    ),
)
def test_card_list_pages_availability(name, args, expected_status,
                                      cards, deck_owner_client):
    url = reverse(name, args=args)
    response = deck_owner_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args, expected_status, redirect_name, redirect_args',
    (
        ('deck:create_card',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'homepage:index',
         None),

        # Фикстуру cards не используем, так что колода пуста
        ('deck:review_display',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'homepage:index',
         None)

    ),
)
def test_card_list_pages_redirects(name, args, expected_status,
                                   redirect_name, redirect_args,
                                   deck,
                                   deck_owner_client):
    url = reverse(name, args=args)
    redirect_url = reverse(redirect_name, args=redirect_args)
    response = deck_owner_client.get(url)
    assert response.status_code == expected_status
    assertRedirects(response, redirect_url)


@pytest.mark.parametrize(
    'name, args, expected_status',
    (
        ('deck:card_list',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.NOT_FOUND),

        ('deck:delete_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.FORBIDDEN),

        ('deck:edit_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.FORBIDDEN),

        ('deck:review_display',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.NOT_FOUND),
    ),
)
def test_card_list_pages_for_other_user(name, args, expected_status,
                                        cards, not_deck_owner_client):
    url = reverse(name, args=args)
    response = not_deck_owner_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args, expected_status, redirect_name, redirect_args',
    (
        ('deck:create_card',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'homepage:index',
         None),
    ),
)
def test_card_list_pages_redirects_for_other_user(name, args, expected_status,
                                                  redirect_name, redirect_args,
                                                  cards,
                                                  not_deck_owner_client):
    url = reverse(name, args=args)
    redirect_url = reverse(redirect_name, args=redirect_args)
    response = not_deck_owner_client.get(url)
    assert response.status_code == expected_status
    assertRedirects(response, redirect_url)


@pytest.mark.parametrize(
    'name, args, expected_status, redirect_name',
    (
        ('deck:card_list',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'login'),

        ('deck:create_card',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'login'),

        ('deck:delete_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.FOUND,
         'login'),

        ('deck:edit_card',
         pytest.lazy_fixture('card_not_in_queue_id_for_args'),
         HTTPStatus.FOUND,
         'login'),

        ('deck:review_display',
         pytest.lazy_fixture('deck_id_for_args'),
         HTTPStatus.FOUND,
         'login'),
    ),
)
def test_card_list_redirects_for_anon(name, args, expected_status, client,
                                      redirect_name,
                                      cards,):
    url = reverse(name, args=args)
    redirect_url = reverse(redirect_name) + '?next=' + url
    response = client.get(url)
    assertRedirects(response, redirect_url)
    assert response.status_code == expected_status
