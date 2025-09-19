from Controllers import BaseController
from Controllers import ProjectController
import os
from langchain.document_loaders import TextLoader, PyMuPDF
from enums import ProcessingEnum

class ProcessController(BaseController):
	def __init__(self, project_id: str) -> None:
		super().__init__()
		self.project_path = ProjectController().create_project(project_id=project_id)

	def get_file_extension(self, file_name: str) -> str:
		return os.path.splitext(file_name)[-1].lower()

	def get_file_loader(self, file_name: str):
		ext = self.get_file_extension(file_name)
		file_path = os.path.join(self.project_path, file_name)
		if ext == ProcessingEnum.TXT.value:
			return TextLoader(file_path, encoding='utf-8')
		elif ext == ProcessingEnum.PDF.value:
			return PyMuPDF(file_path)
		else:
			return None
