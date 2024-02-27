import pytest


@pytest.fixture()
def base_url():
    base_url = 'https://reqres.in/api'
    return base_url
