from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal
import os
from pathlib import Path

class ProjectController(BaseController):
    def __init__(self) -> None:
        super().__init__()


    async def create_project(self, project_id: str) -> str:
        """
        Create a new project folder under assets/files/.
        """
        project_path = os.path.join(self.files_path, project_id)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            return project_path
        return project_path

    async def check_if_file_exists(self, project_id: str, filename: str) -> bool:
        """
        Check if a file exists in the specified project folder.
        """
        project_path = Path(self.files_path) / project_id
        files = [f.name for f in project_path.iterdir() if f.is_file()]
        for f in files:
            if f[12:] == filename[12:]:  # Compare only the original filename part
                return True
        return False
