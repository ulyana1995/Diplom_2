import requests
from config import CREATE_USER_ENDPOINT, USER_DATA_ENDPOINT, LOGIN_USER_ENDPOINT

def create_user(payload):
    return requests.post(CREATE_USER_ENDPOINT, json=payload)

def delete_user(token):
    headers = {
        "Authorization": token
    }   
    return requests.delete(USER_DATA_ENDPOINT, headers=headers)

def login_user(payload):  
    return requests.post(LOGIN_USER_ENDPOINT, json=payload)

def update_user(payload, token=None):
    headers = None
    if token is not None:
        headers = {
            "Authorization": token
        }              
    return requests.patch(USER_DATA_ENDPOINT, json=payload, headers=headers)
