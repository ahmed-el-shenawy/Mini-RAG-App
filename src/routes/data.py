from fastapi import APIRouter, UploadFile,status
from fastapi.responses import JSONResponse
from core.config import settings
from controllers import DataController
from models import ResponseSignal

data_router = APIRouter(
	prefix="/api/v1/data",
	tags=["Base"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile):
	result = await DataController().validate_file(file=file)
	if not result["state"]:
		match result["error_code"]:
			case ResponseSignal.FILE_TYPE_INVALID:
				return JSONResponse(
					status_code=status.HTTP_400_BAD_REQUEST,
					content={
					"status": "Failed",
					"message": f"Invalid file type '{file.content_type}'. Allowed types: {settings.FILE_ALLOWED_TYPES}",
					})
			case ResponseSignal.FILE_SIZE_EXCEEDED:
				return JSONResponse(
					status_code=status.HTTP_400_BAD_REQUEST,
					content={
					"status": "Failed",
					"message": f"File size exceeds maximum limit of {settings.FILE_MAX_SIZE} MB.",
					})
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={
		"status": "Success",
		"message": ResponseSignal.FILE_UPLOAD_SUCCESS,
		"project_id": project_id,
		"filename": file.filename,
		})
