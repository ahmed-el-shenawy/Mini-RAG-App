
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)
from pymongo import InsertOne

from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunks
from .enums import DatabaseEnum


class ChunksModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client=db_client)
        self.collection: AsyncIOMotorCollection = self.db_client[DatabaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorClient):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection: AsyncIOMotorCollection = self.db_client[
                DatabaseEnum.COLLECTION_CHUNK_NAME.value
            ]
            indexes = DataChunks.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_chunk(self, chunk: DataChunks):
        result = await self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude_none=True)
        )
        chunk.id = result.inserted_id

    async def create_many_chunks(self, chunks: list[DataChunks], patch_size: int = 100):
        for i in range(0, len(chunks), patch_size):
            patch: list[DataChunks] = chunks[i : i + patch_size]
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_none=True))
                for chunk in patch
            ]
        await self.collection.bulk_write(operations)
        return len(chunks)

    async def get_chunk(self, chunk_id: ObjectId):
        chunk_id = ObjectId(chunk_id)
        result = await self.collection.find_one({"_id": chunk_id})
        if not result:
            return None
        return DataChunks(**result)

    async def get_all_chunks(self, page: int, page_size: int):
        total_documents_count = await self.collection.count_documents({})
        total_pages = total_documents_count // page_size
        if total_documents_count % page_size > 0:
            total_pages += 1
        skip_boundry = (page - 1) * page_size
        cursor = self.collection.find().skip(skip_boundry).limit(page_size)
        chunks = []
        async for document in cursor:
            chunks.append(DataChunks(**document))
        return chunks, total_pages

    async def del_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
