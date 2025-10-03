from providers import QdrantDB
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController

class VectorDBProviderFactory():
    def __init__(self,config) -> None:
        self.config = config
        self.base_controller = BaseController()

    def create_provider(self,provider_type:str):
        if provider_type == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_db_path(self.config.QDRANT_DB_PATH)
            return QdrantDB(
                db_path=db_path,
                distance_metric=self.config.VECTOR_DB_METRIC
            )
        else:
            return None