from motor.motor_asyncio import AsyncIOMotorDatabase

from core import settings
from core.config import Settings


class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorDatabase):
        self.db_client: AsyncIOMotorDatabase = db_client
        self.settings: Settings = settings
