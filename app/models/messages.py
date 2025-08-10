from datetime import datetime
from app.extensions import mongo

class MessageModel:
    @staticmethod
    def create(message, role, chat_id):
        doc = {
            "chat_id": chat_id,
            "message": message,
            "role": role,
            "created_at": datetime.utcnow()
        }
        return mongo.db.messages.insert_one(doc).inserted_id

    @staticmethod
    def get_all():
        return list(mongo.db.messages.find().sort("created_at", 1))

    @staticmethod
    def delete_all():
        return mongo.db.messages.delete_many({})
    
    @staticmethod
    def get_messages_by_chat_id(chatId):
        return mongo.db.messages.find({"chat_id":chatId}).sort("created_at", 1)
    
    @staticmethod
    def update_by_chat_id(chatId, message):
        return mongo.db.messages.update_one({"chat_id":chatId},{"$set": {"message": message}},upsert=True)
