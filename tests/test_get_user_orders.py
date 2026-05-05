from api.order_api import create_order, get_orders
from data.user_data import build_order_payload
from constants.http_codes import HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED
from constants.messages import ERROR_UNAUTHORIZED
import allure

class TestGetUserOrder:
    @allure.title("Авторизованный пользователь может получить список заказов")
    def test_get_orders_authorized_user_success(self, created_user, ingredients_list):
        payload = build_order_payload(ingredients_list[0])       
        
        with allure.step("Создаём заказ для проверки списка заказов"):        
            create_order(payload, created_user["token"])

        with allure.step("Отправляем запрос на получение заказов"):
            response = get_orders(created_user["token"])

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_OK}"):
            assert response.status_code == HTTP_STATUS_OK

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):        
            assert "orders" in response_data
            assert "total" in response_data
            assert "totalToday" in response_data
            assert isinstance(response_data["orders"], list)
            assert len(response_data["orders"]) == 1

    @allure.title("Неавторизованный пользователь не может получить заказы")
    def test_get_orders_unauthorized_fail(self):
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = get_orders()

        with allure.step(f"Проверяем статус код = {HTTP_STATUS_UNAUTHORIZED}"):
            assert response.status_code == HTTP_STATUS_UNAUTHORIZED

        with allure.step("Получаем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем структуру и значения тела ответа"):        
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_UNAUTHORIZED
