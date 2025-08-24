import os

class Config:
    API_KEY = os.getenv("API_KEY")  # Default API key (override with env vars)
    SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key for session management
