import allure
import pytest
import requests
import jsonschema
from .schemas.store_schema import STORE_SCHEMA
from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_post_order(self):
        with allure.step("Отправить запрос на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, STORE_SCHEMA)
        with allure.step("Проверка содержания данных заказа"):
            assert response_json['id'] == payload['id'], "id store не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId store не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity store не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status store не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete store не совпадает с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order(self, create_store):
        with allure.step("Создание и получение питомца с id=1"):
            store_id = create_store['id']
        with allure.step("Отправить запрос на получение информации о заказе"):
            response = requests.get(f'{BASE_URL}/store/order/{store_id}')
            response_json = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, STORE_SCHEMA)
        with allure.step("Проверка содержания данных заказа"):
            assert response_json['id'] == create_store['id'], "id store не совпадает с ожидаемым"
            assert response_json['petId'] == create_store['petId'], "petId store не совпадает с ожидаемым"
            assert response_json['quantity'] == create_store['quantity'], "quantity store не совпадает с ожидаемым"
            assert response_json['status'] == create_store['status'], "status store не совпадает с ожидаемым"
            assert response_json['complete'] == create_store['complete'], "complete store не совпадает с ожидаемым"


    @allure.title("Удаление заказа по ID")
    def test_delete_store_for_id(self, create_store):
        with allure.step("Создание и получение питомца с id=1"):
            store_id = create_store['id']
        with allure.step("Отправить запрос на удаление питомца"):
            response = requests.delete(f'{BASE_URL}/store/order/{store_id}')
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
        with allure.step("Отправить запрос на получение несуществующего заказа"):
            response = requests.get(f'{BASE_URL}/store/order/{store_id}')
        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_store(self):
        with allure.step("Отправить запрос на получение несуществующего заказа"):
            response = requests.get(f'{BASE_URL}/store/order/9999')
        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправить запрос на получение данных инвентаря"):
            response = requests.get(f'{BASE_URL}/store/inventory')
        with allure.step("Проверка статус кода и тела ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)