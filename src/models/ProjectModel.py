from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)

from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums import DatabaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorClient):
        print("11")
        super().__init__(db_client=db_client)
        self.collection: AsyncIOMotorCollection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorClient):
        print("12")
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        print("13")
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection: AsyncIOMotorCollection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_project(self, project_id: str) -> Project:
        project = Project(project_id=project_id)
        result = await self.collection.insert_one(
            project.model_dump(by_alias=True, exclude_none=True)
        )
        project.id = result.inserted_id
        print(project)
        return project

    async def get_project_or_create_one(self, project_id: str):
        print("shn4")
        record = await self.collection.find_one({"project_id": project_id})
        print("shn5")
        print(record)
        print("shn6")
        if not record:
            project: Project = await self.create_project(project_id=project_id)
            return project
        # project = Project(project_id=project_id, id=record["id"])
        project = Project(**record)
        print(project)
        print("shn7")
        return project

    async def get_all_projects(self, page: int = 1, page_size: int = 20):
        total_documents_count = await self.collection.count_documents({})
        total_pages = total_documents_count // page_size
        if total_documents_count % page_size > 0:
            total_pages += 1
        skip_boundry = (page - 1) * page_size
        cursor = self.collection.find().skip(skip_boundry).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))
        return projects, total_pages
