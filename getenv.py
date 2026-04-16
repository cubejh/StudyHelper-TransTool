from dotenv import load_dotenv, set_key
import os

load_dotenv()

def get_api_key():
    return os.getenv("API_KEY")

def get_models():
    models = os.getenv("MODEL", "")
    return [m.strip() for m in models.split(",") if m.strip()]

def get_other_model():
    return os.getenv("OTHER_MODEL")

def set_api_key(api_key):
    set_key(".env", "API_KEY", api_key)


def add_model(model_name):
    models = get_models()

    if model_name not in models:
        models.append(model_name)
        new_value = ",".join(models)
        set_key(".env", "MODEL", new_value)


def delete_model(model_name):
    models = get_models()

    if model_name in models:
        models.remove(model_name)
        new_value = ",".join(models)
        set_key(".env", "MODEL", new_value)