import pytest

from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, expected_status',
    (
        ('registration', HTTPStatus.OK),
        ('login', HTTPStatus.OK),
        ('logout', HTTPStatus.OK),
        ('password_reset', HTTPStatus.OK),
        ('password_reset_done', HTTPStatus.OK)

    ),
)
def test_public_pages_availability(client, name, expected_status):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        'password_change',
        'password_change_done'

    ),
)
def test_public_pages_redirects(client, name):
    url = reverse(name)
    expected_url = f'/auth/login/?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
