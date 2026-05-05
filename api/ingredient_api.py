import requests
from config import INGREDIENTS_ENDPOINT

def get_ingredients():
    return requests.get(INGREDIENTS_ENDPOINT)
