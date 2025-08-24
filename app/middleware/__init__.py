import os
import jwt
from flask import request, current_app
from functools import wraps
from loguru import logger
from flask import g

# Function to validate API Key
def validate_api_key(request):
    api_key = request.headers.get('Authorization')
    if not api_key:
        return False
    secret_key = current_app.config.get("SECRET_KEY", "default_secret_key")
    try:
        decoded = jwt.decode(api_key, secret_key, algorithms=["HS256"])
        g.public_id = decoded.get("public_id")
        logger.debug(f"Decoded JWT: {decoded}")
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return True

# Auth Middleware
def auth_middleware():
    if request.path.startswith('/auth'):
        return
    if not validate_api_key(request):
        return {"error": "Unauthorized"}, 401
    
# Decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not validate_api_key(request):
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated