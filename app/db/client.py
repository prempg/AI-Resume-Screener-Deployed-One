from pymongo import AsyncMongoClient
from app.config import settings

mongo_client: AsyncMongoClient = AsyncMongoClient(settings.MONGO_URI)

