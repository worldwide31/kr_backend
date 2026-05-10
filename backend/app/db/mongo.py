from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


@lru_cache
def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongo_url)


def get_mongo_db() -> AsyncIOMotorDatabase:
    return get_mongo_client()[settings.mongo_db]

