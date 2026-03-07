from dotenv import load_dotenv, set_key
import os

load_dotenv()

def get_api_key():
    """get api key"""
    return os.getenv("API_KEY")


def get_models():
    """get gemini model (return list)"""
    models = os.getenv("MODEL", "")
    return [m.strip() for m in models.split(",") if m.strip()]


def get_other_model():
    """get other model"""
    return os.getenv("OTHER_MODEL")

def set_api_key(api_key):
    set_key(".env","API_KEY", api_key)