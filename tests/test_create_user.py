from api.user_api import create_user, delete_user
from data.user_data import generate_user_data
from constants.http_codes import HTTP_STATUS_OK, HTTP_STATUS_FORBIDDEN
from constants.messages import ERROR_USER_ALREADY_EXISTS, ERROR_MISSING_FIELD
from steps.create_user_steps import create_new_user
import allure
import pytest

class TestCreateUser:
    @allure.title("Создание нового пользователя")
    def test_create_unique_user_is_successful(self):
        payload = generate_user_data()
    
        with allure.step("Отправка запроса на создание пользователя"):
            response = create_user(payload)

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["success"] is True
            assert response_data["user"]["email"] == payload["email"]
            assert response_data["user"]["name"] == payload["name"]

        with allure.step("Удаление созданного пользователя"):
            delete_user(response_data.get("accessToken"))    

    @allure.title("Создание уже существующего пользователя возвращает ошибку")
    def test_create_duplicate_user_error(self, created_user):
        with allure.step("Отправка запроса на создание пользователя с существующими данными пользователя"):
            response = create_new_user(created_user["email"], created_user["password"], created_user["name"])

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_FORBIDDEN}"):
            assert response.status_code == HTTP_STATUS_FORBIDDEN

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["success"] is False 
            assert response_data["message"] == ERROR_USER_ALREADY_EXISTS 

    @allure.title("Создание пользователя без поля")                     
    @pytest.mark.parametrize('missing_field', [
        "email",
        "password",
        "name"       
    ])
    def test_create_user_missing_field_fail(self, missing_field):
        payload = generate_user_data()
    
        payload.pop(missing_field)

        with allure.step(f"Отправка запроса без поля {missing_field}"):
            response = create_user(payload)      

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_FORBIDDEN}"):
            assert response.status_code == HTTP_STATUS_FORBIDDEN

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["success"] is False 
            assert response_data["message"] == ERROR_MISSING_FIELD 
