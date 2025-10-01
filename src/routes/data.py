import logging
import os

import aiofiles
from bson import ObjectId
from fastapi import APIRouter, Request, UploadFile, status
from fastapi.responses import JSONResponse

from controllers import DataController, ProcessController, ProjectController
from core.config import settings
from models import AssetModel, ChunksModel, ProjectModel
from models.db_schemes.asset import Asset
from models.db_schemes.data_chunks import DataChunks
from models.db_schemes.project import Project
from models.enums import ResponseSignal

from .schemes import ProcessRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Base"],
)


@data_router.post("/process/{project_id}")
async def process_data(
    project_id: str, process_request: ProcessRequest, request: Request
):
    try:
        print("shn1")
        project_model = await ProjectModel.create_instance(
            db_client=request.app.db_client
        )
        print("shn2")
        chunk_model = await ChunksModel.create_instance(db_client=request.app.db_client)
        print("shn3")

        project: Project = await project_model.get_project_or_create_one(
            project_id=project_id
        )

        # if process_request.do_reset:
        #     await chunk_model.del_chunks_by_project_id(project_id=project.id)
        # print(project)
        asset_model = await AssetModel.create_instance(
            db_client=request.app.db_client
        )
        print("t")
        print(project.id)
        docs = []
        # if process_request.file_id:
        #     print("here1")
        #     assets_list = await asset_model.get_all_project_assets(asset_project_id=project.id,file_id=process_request.file_id)
        #     print(assets_list)
        #     if assets_list:
        #         for asset in assets_list:
        #             print("shnn")
        #             process_controller = ProcessController(project_id=project_id)
        #             processed_docs = await process_controller.process_file_content(
        #                 project_id=project_id, file_name= asset
        #             )
        #             docs.append(processed_docs)
        # else:
        print("here2")
        assets_list = await asset_model.get_all_project_assets(asset_project_id=project.id,file_id=process_request.file_id)
        if assets_list:
            for asset in assets_list:
                print("shnn_asset")
                print(asset)
                process_controller = ProcessController(project_id=project_id)
                processed_docs = await process_controller.process_file_content(
                    project_id=project_id, file_name=asset.asset_name)
                docs.append(processed_docs)
            print(docs)
        print("shnn8")
        if not docs:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "Failed",
                    "message": f"Failed to process file ID {process_request} in project {project_id}.",
                },
            )
        else:
            if process_request.do_reset:
                await chunk_model.del_chunks_by_project_id(project_id=project.id)
            print(project)

            file_chunks_record = [
                [DataChunks(
                    chunk_text=chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order=i + 1,
                    chunk_project_id=project.id,
                )
                for i, chunk in enumerate(processed_docs)] for processed_docs in docs
            ]
            data = []
            for file_rec in file_chunks_record:
                result = await chunk_model.create_many_chunks(chunks=file_rec)
                data.append(result)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "Success",
                    "message": f"Data processing initiated for file ID  in project {project_id}.",
                    "n_of_chunks": data,
                    # "chunk_size": process_request.chunk_size,
                    # "overlap": process_request.overlap,
                    # "do_reset": process_request.do_reset,
                    # "docs": [
                    #     {"content": doc.page_content, "metadata": doc.metadata}
                    #     for doc in processed_docs
                    # ],
                },
            )
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "Failed", "message": "Error processing data"},
        )


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile):
    try:
        print("s1")
        project_model = await ProjectModel.create_instance(
            db_client=request.app.db_client
        )
        print("s")
        project: Project = await project_model.get_project_or_create_one(
            project_id=project_id
        )
        print(project)
        print(project.id)
        print(type(project.id))
        print("s2")
        # Validate file

        result = await DataController().validate_file(file=file)
        if not result["state"]:
            match result["error_code"]:
                case ResponseSignal.FILE_TYPE_INVALID:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "status": "Failed",
                            "message": f"Invalid file type '{file.content_type}'. Allowed types: {settings.FILE_ALLOWED_TYPES}",
                        },
                    )
                case ResponseSignal.FILE_SIZE_EXCEEDED:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "status": "Failed",
                            "message": f"File size exceeds maximum limit of {settings.FILE_MAX_SIZE} MB.",
                        },
                    )

        # Reset file position after validation
        await file.seek(0)

        # Create project folder if not exists
        project_path = ProjectController().create_project(project_id=project_id)
        # Check if file already exists in the project
        file_name = await DataController().genrate_unique_filename(
            original_filename=file.filename, project_id=project_id
        )
        file_name = str(file_name).lower()
        file_exists = await ProjectController().check_if_file_exists(
            project_id=project_id, filename=file_name
        )
        if file_exists:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "Failed",
                    "message": f"File with name '{file_exists}' already exists in project '{project_id}'. Please rename your file and try again.",
                },
            )

        # Generate unique filename

        file_path = os.path.join(project_path, file_name)

        # Save file to disk using aiofiles
        print("6")
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(settings.FILE_DEFAULT_CHUNK_SIZE)
                if not chunk:
                    break
                await f.write(chunk)
                await f.flush()  # Ensure data is written to disk
        print("66")
        asset_model = await AssetModel.create_instance(
            db_client=request.app.db_client
        )
        print("67")
        print(ObjectId(project.id))
        asset_resource = Asset(
            asset_project_id=project.id,
            asset_name= file_name,
            asset_type=file.content_type,
            asset_size=os.path.getsize(file_path)
        )
        print("7")
        await asset_model.create_asset(asset_resource)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "Success",
                "message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "project_id": str(project.id),
                "filename": file.filename,
                "saved_as": file_name,
                "file_path": file_path,
            },
        )

    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "Failed", "message": "Error uploading file "},
        )
    finally:
        await file.close()  # Ensure file is closed
