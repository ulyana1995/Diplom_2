from api.ingredient_api import get_ingredients
from api.user_api import delete_user, create_user
from data.user_data import generate_user_data
import allure
import pytest 

@pytest.fixture
def created_user():
    with allure.step("Генерация данных пользователя"):
        user_data = generate_user_data()
        email = user_data["email"]
        password = user_data["password"]
        name = user_data["name"]

    with allure.step("Создание пользователя через API"):    
        response = create_user(user_data)
        response_data = response.json()
        token = response_data.get("accessToken")
    yield {
        "email": email,
        "password": password,
        "name": name,
        "token": token,
        "response": response     
    }
    with allure.step("Удаление пользователя"):
        if token:
            delete_user(token)

@pytest.fixture
def ingredients_list():
    with allure.step("Получение списка ингредиентов"):
        response = get_ingredients()
    
    response_data = response.json()

    with allure.step("Формирование списка ID ингредиентов"):
        list_ingredients_ids = []
        for item in response_data["data"][:5]:
            list_ingredients_ids.append(item["_id"])
    return list_ingredients_ids
