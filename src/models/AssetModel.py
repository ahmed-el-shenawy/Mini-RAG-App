from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)

from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums import DatabaseEnum


class AssetModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client=db_client)
        self.collection: AsyncIOMotorCollection = self.db_client[
            DatabaseEnum.COLLECTION_ASSET_NAME.value
        ]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorClient):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection: AsyncIOMotorCollection = self.db_client[
                DatabaseEnum.COLLECTION_ASSET_NAME.value
            ]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_none=True))
        asset.id = result.inserted_id

    async def get_all_project_assets(self, asset_project_id: ObjectId, file_id:str):
        print("t5")
        if file_id:
            result =await self.collection.find_one({"asset_project_id": asset_project_id, "asset_name":file_id})
            if not result:
                return None
            print("result")
            result = [Asset(**result)]
            print(result)
            return result
        else:
            cursor = self.collection.find({"asset_project_id": asset_project_id})
            result = await cursor.to_list(length=None)
            print("t5")
            print(result)
            if not result:
                return None
            return [Asset(**re) for re in result]
