from api.user_api import update_user
from data.user_data import generate_user_data
from constants.http_codes import HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED
from constants.messages import ERROR_UNAUTHORIZED
import allure
import pytest

class TestUpdateUserData:
    @allure.title("Обновление данных пользователя с авторизацией") 
    @pytest.mark.parametrize('updating_field', [
            ("email",),
            ("password",),
            ("name",), 
            ("email", "password"),
            ("email", "name"),
            ("password", "name"),
            ("email", "password", "name")       
        ])
    def test_update_user_fields_with_auth_success(self, created_user, updating_field):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        }
        
        new_data = generate_user_data()

        for field in updating_field:
            payload[field] = new_data[field]

        with allure.step("Отправка запроса на обновление пользователя"):
            response = update_user(payload, created_user["token"])
        
        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):  
            assert response_data["success"] is True        
            assert response_data["user"]["email"] == payload["email"]
            assert response_data["user"]["name"] == payload["name"]

    @allure.title("Обновление данных пользователя без авторизацией") 
    @pytest.mark.parametrize('updating_field', [
            ("email",),
            ("password",),
            ("name",) 
    ])
    def test_update_user_data_without_auth_error(self, created_user, updating_field):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        }

        new_data = generate_user_data()

        for field in updating_field:
            payload[field] = new_data[field]

        with allure.step("Отправка запроса на обновление пользователя без токена"):
            response = update_user(payload)

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_UNAUTHORIZED}"):
            assert response.status_code == HTTP_STATUS_UNAUTHORIZED

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"): 
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_UNAUTHORIZED          
