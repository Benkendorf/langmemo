import pytest

from http import HTTPStatus

from django.urls import reverse



@pytest.mark.parametrize(
    'name, expected_status',
    (
        ('deck:card_list', HTTPStatus.OK),
        ('deck:create_card', HTTPStatus.OK),
        ('deck:delete_card', HTTPStatus.OK),
        ('deck:review_display', HTTPStatus.OK),
        ('deck:review_check', HTTPStatus.OK)    #Тут надо проверить на карте в очереди, и нет

    ),
)
def test_card_list_pages_availability(name, expected_status, cards):
    #url = reverse('homepage:index')
    #response = parametrized_client.get(url)
    #assert response.status_code == expected_status