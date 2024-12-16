import pytest


@pytest.fixture
def registration_data():
    return {'username': 'test_user',
            'password1': 'zwerty789',
            'password2': 'zwerty789'}
