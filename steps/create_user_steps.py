from data.user_data import build_create_user_payload
from api.user_api import create_user

def create_new_user(email, password, name):
    payload = build_create_user_payload(email, password, name)
    response = create_user(payload)
    return response
