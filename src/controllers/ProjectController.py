from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal
import os

class ProjectController(BaseController):
    def __init__(self) -> None:
        super().__init__()


    async def create_project(self, name: str) -> str:
        """
        Create a new project folder under assets/files/.
        """
        project_path = os.path.join(self.files_path, name)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            return project_path
        return project_path
