import allure
import requests

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
