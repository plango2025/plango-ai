from pymongo import MongoClient
from app.config.settings import settings

# MongoClient 싱글턴 객체
client = MongoClient(settings.MONGO_URI)

# 사용할 데이터베이스 객체
db = client[settings.MONGO_DB_NAME]
