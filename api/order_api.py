from config import ORDERS_ENDPOINT
import requests

def create_order(payload, token=None):
    headers = None
    if token is not None:
        headers = {
            "Authorization": token
        } 
    return requests.post(ORDERS_ENDPOINT, json=payload, headers=headers)

def get_orders(token=None):
    headers = None    
    if token is not None:
        headers = {
            "Authorization": token
        }     
    return requests.get(ORDERS_ENDPOINT, headers=headers)