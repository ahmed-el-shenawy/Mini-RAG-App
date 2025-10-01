import logging
from .BaseController import BaseController
from .ProjectController import ProjectController
from pathlib import Path
from models import ProcessingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


class ProcessController(BaseController):
    def __init__(self, project_id: str) -> None:
        super().__init__()
        self.project_path = ProjectController().create_project(project_id=project_id)

    def get_file_extension(self, file_name: str) -> str:
        result = os.path.splitext(file_name)[-1].lower()
        logging.info(f"File extension: {result}")
        return result

    def get_file_loader(self, file_name: str):
        ext = self.get_file_extension(file_name)
        file_path = Path(self.project_path) / file_name
        if ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            return None

    def get_file_content(self, file_name: str):
        loader = self.get_file_loader(file_name)
        if loader:
            return loader.load()
        else:
            return None

    async def process_file_content(self, project_id: str, file_name: str):
        file_exist = await ProjectController().check_if_file_exists(
            project_id=project_id, filename=file_name
        )
        if not file_exist:
            return None
        docs = self.get_file_content(file_name)
        if docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.settings.FILE_DEFAULT_CHUNK_SIZE,
                chunk_overlap=20,
                length_function=len,
            )
            split_docs: list = text_splitter.split_documents(docs)
            print(f"Number of split documents: {len(split_docs)}")
            return split_docs
        else:
            return None
