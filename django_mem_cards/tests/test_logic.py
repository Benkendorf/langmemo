import pytest

from pytest_django.asserts import assertRedirects
from django.urls import reverse
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


@pytest.mark.django_db
def test_anon_can_signup(client, registration_data):
    url = reverse('registration')
    redirect_url = reverse('homepage:index')
    response = client.post(url, data=registration_data)
    assertRedirects(response, redirect_url)
    assert CustomUser.objects.count() == 1
    user = CustomUser.objects.get()
    assert user.username == registration_data['username']
    
    # Возможно вручную зашифровать пароль и сравнить с тем, что лежит в БД
    # Также проверить смену пароля
