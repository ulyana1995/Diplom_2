from api.user_api import login_user
from constants.messages import ERROR_INVALID_CREDENTIALS
from constants.http_codes import HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED
from data.user_data import build_login_user_payload
import allure
import pytest

class TestLoginUser:
    @allure.title("Успешная авторизация зарегистрированного пользователя")  
    def test_login_existing_user_success(self, created_user):
        email = created_user["email"]
        password = created_user["password"]
        name = created_user["name"]

        payload = build_login_user_payload(email, password)

        with allure.step("Отправка запроса на логин пользователя"):       
            response = login_user(payload) 

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):   
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert response_data["user"]["email"] == email
            assert response_data["user"]["name"] == name          


    @allure.title("Логин с неверными данными")
    @pytest.mark.parametrize('incorrect_fields', [
        ("email",),
        ("password",),
        ("email", "password"),
    ])
    def test_login_with_incorrect_credentials_error(self, created_user, incorrect_fields):
        email = created_user["email"]
        password = created_user["password"]

        payload = build_login_user_payload(email, password)

        for field in incorrect_fields:
            payload[field] = payload[field] + "1"

        with allure.step("Отправка запроса на логин"):
            response = login_user(payload) 

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_UNAUTHORIZED}"):
            assert response.status_code == HTTP_STATUS_UNAUTHORIZED

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):  
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_INVALID_CREDENTIALS       
