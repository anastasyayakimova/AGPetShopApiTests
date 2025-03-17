import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправить DELETE-запрос"):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')
            print(response)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
        with allure.step("Проверка текста ошибки"):
            assert response.text == "Pet deleted", "текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправить PUT-запрос на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
                }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"
        with allure.step("Проверка текста ошибки"):
            assert response.text == "Pet not found", "текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправить GET-запрос на получение информации о несуществующем питомце"):
            response = requests.get(url=f'{BASE_URL}/pet/9999')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"
        with allure.step("Проверка текста ошибки"):
            assert response.text == "Pet not found", "текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_create_pet(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_create_pet_with_all_payload(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{"id": 0,
                          "name": "string"}],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response_json['category']['id'] == payload['category']['id'], "id категории питомца не совпадает с ожидаемым"
            assert response_json['category']['name'] == payload['category']['name'], "name категории питомца не совпадает с ожидаемым"
            assert response_json['tags'][0]['id'] == payload['tags'][0]['id'], "id тега категории питомца не совпадает с ожидаемым"
            assert response_json['tags'][0]['name'] == payload['tags'][0]['name'], "name тега категории питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'][0] == payload['photoUrls'][0], "фото питомца не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_for_id(self, create_pet):
        with allure.step("Получить id созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Отправка запроса на получение информации о питомце"):
            response = requests.get(f'{BASE_URL}/pet/{pet_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            assert response.json()['id'] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_for_id(self, create_pet):
        with allure.step("Получить id созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Подготовить данные для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
                }
        with allure.step("Отправить запрос на обновление питомца"):
            response = requests.put(f'{BASE_URL}/pet', json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            assert response.json()['id'] == pet_id
            assert response.json()['name'] == payload['name']
            assert response.json()['status'] == payload['status']

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_for_id(self, create_pet):
        with allure.step("Получить id созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Отправить запрос на удаление питомца"):
            response = requests.delete(f'{BASE_URL}/pet/{pet_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
        with allure.step("Отправить запрос на получение информации о питомце по id"):
            response = requests.get(f'{BASE_URL}/pet/{pet_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"