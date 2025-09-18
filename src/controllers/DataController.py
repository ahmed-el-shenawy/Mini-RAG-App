from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal

class DataController(BaseController):
	def __init__(self) -> None:
		super().__init__()
		self.scale_size =  1024 * 1024  # Scale size to MB
		# You can access settings via self.settings
		# e.g., self.settings.APP_NAME
	async def validate_file(self, file: UploadFile) -> dict:
		# Validate file type and size based on settings
		if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
			return {
                    "state": False,
                    "error_code": ResponseSignal.FILE_TYPE_INVALID,
                }
		contents = await file.read()
		size = len(contents)
		if size > self.settings.FILE_MAX_SIZE * self.scale_size:
			return {
                    "state": False,
                    "error_code": ResponseSignal.FILE_SIZE_EXCEEDED,
                }
		return {
                "state": True,
            }
