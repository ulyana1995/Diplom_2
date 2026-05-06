from utils.helpers import generate_random_email, generate_random_password, generate_random_name

def generate_user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),       
        "name":generate_random_name() 
    }

def build_create_user_payload(email=None, password=None, name=None):    
    return {
        "email": email,
        "password": password,
        "name": name
    }

def build_login_user_payload(email, password):  
    return {
        "email": email,
        "password": password
    }

def build_order_payload(ingredients):
    return {
        "ingredients": ingredients
    }
