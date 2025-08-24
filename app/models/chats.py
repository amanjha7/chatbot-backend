from datetime import datetime
from app.extensions import mongo

class ChatModel:
    @staticmethod
    def create(title, chatId, user_id=None):
        doc = {
            "chat_id": chatId,
            "title": title,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }
        return mongo.db.chats.insert_one(doc).inserted_id

    @staticmethod
    def get_all(user_id=None):
        return list(mongo.db.chats.find({"user_id":user_id}).sort("created_at", -1))

    @staticmethod
    def get_by_id(chat_id):
        return mongo.db.chats.find_one({"chat_id": chat_id})

    @staticmethod
    def delete_all():
        return mongo.db.chats.delete_many({})

    @staticmethod
    def delete_by_id(chat_id):
        return mongo.db.chats.delete_one({"chat_id": chat_id})
