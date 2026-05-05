from api.order_api import create_order
from data.user_data import build_order_payload
from constants.http_codes import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_INTERNAL_SERVER_ERROR
from constants.messages import ERROR_MESSAGE_EMPTY_INGREDIENTS
import allure

class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")  
    def test_create_order_authorized_user_success(self, created_user, ingredients_list):
        payload = build_order_payload(ingredients_list[0])

        with allure.step("Отправка запроса на создание заказа"):
            response = create_order(payload, created_user["token"])

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data.get("success") is True    
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]
 
    @allure.title("Неавторизованный пользователь может создать заказ")  
    def test_create_order_unauthorized_user_success(self, ingredients_list):
        """Возможно создать заказ для неавторизованного пользователя"""
        payload = build_order_payload(ingredients_list[0])

        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = create_order(payload)

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK 

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["success"] is True    
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Создание заказа с несколькими ингредиентами")
    def test_create_order_with_multiple_ingredients_success(self, created_user, ingredients_list):
        payload = build_order_payload(ingredients_list)        
        
        with allure.step("Отправка запроса на создание заказа с несколькими ингредиентами"):
            response = create_order(payload, created_user["token"])
        
        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["success"] is True    
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Создание заказа без ингредиентов возвращает ошибку")
    def test_create_order_no_ingredients(self, created_user):
        payload = {"ingredients": []}
        
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = create_order(payload, created_user["token"])

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_BAD_REQUEST}"):
            assert response.status_code == HTTP_STATUS_BAD_REQUEST

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):
            assert response_data["message"] == ERROR_MESSAGE_EMPTY_INGREDIENTS

    @allure.title("Создание заказа с невалидным хэшем возвращает ошибку")
    def test_create_order_invalid_hash(self, created_user, ingredients_list):
        invalid_hash = ingredients_list[0] + "123"

        payload = build_order_payload([invalid_hash]) 

        with allure.step("Отправка запроса с невалидным хэшем ингредиента"):
            response = create_order(payload, created_user["token"])

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_INTERNAL_SERVER_ERROR}"):
            assert response.status_code == HTTP_STATUS_INTERNAL_SERVER_ERROR

        with allure.step("Проверяем тело ответа"):
            assert "Error" in response.text


