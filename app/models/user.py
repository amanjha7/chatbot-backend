from datetime import datetime
from app.extensions import mongo
from app.utils.common_utils import generate_uuid, hash_string

class UserModel:
    @staticmethod
    def create(username, email, password):
        doc = {
            "id" : generate_uuid(),
            "username": username,
            "email": email,
            "password": hash_string(password),
            "created_at": datetime.utcnow()
        }
        mongo.db.users.insert_one(doc)
        return doc["id"]
    
    @staticmethod
    def validate_user(password, email):
        user = mongo.db.users.find_one({"password": hash_string(password), "email": email})
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({"id": user_id},{"password": 0})
    
    @staticmethod
    def check_user_exists(email):
        user = mongo.db.users.find_one({"email": email})
        return user is not None