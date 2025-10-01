from .BaseController import BaseController
from pathlib import Path
from models import ProjectModel
import logging


class ProjectController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def create_project(self, project_id: str) -> str:
        """
        Create a new project folder under assets/files/. if not exist, and return the path.
        """
        project_path = Path(self.files_path) / project_id
        if not project_path.exists():
            project_path.mkdir(parents=True, exist_ok=True)
        return str(project_path)

    async def check_if_file_exists(self, project_id: str, filename: str) -> bool | str:
        """
        Check if a file exists in the specified project folder.
        """
        project_path = Path(self.files_path) / project_id
        files = [f.name for f in project_path.iterdir() if f.is_file()]
        for f in files:
            if f[12:] == filename[12:]:  # Compare only the original filename part
                return f
        return False
