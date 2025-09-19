from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os
from .ProjectController import ProjectController

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
	# Generate a random string for filename uniqueness
	async def genrate_unique_filename(self, original_filename: str, project_id: str) -> str:
		random_file_name = self.generate_random_string()
		cleaned_name = await self.get_cleaned_filename(original_filename)
		unique_filename = f"{random_file_name}_{cleaned_name}"
		project_path = await ProjectController().create_project(project_id=project_id)
		while os.path.exists(os.path.join(project_path, unique_filename)):
			random_file_name = self.generate_random_string()
			unique_filename = f"{random_file_name}_{cleaned_name}"
		print(unique_filename)
		return unique_filename

	async def get_cleaned_filename(self, filename: str) -> str:
		# Clean the filename to prevent security issues
		cleaned_name = re.sub(r'[^a-zA-Z0-9_.-]', "_", filename)
		print(cleaned_name)
		return cleaned_name
