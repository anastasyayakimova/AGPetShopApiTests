import pytest
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@pytest.fixture(scope="function") #область видимости
def create_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}/pet', json=payload)
    assert response.status_code == 200
    return response.json()