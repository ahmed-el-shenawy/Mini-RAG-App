from ..VectorDBInterface import VectorDBInterface
from qdrant_client import QdrantClient, models
from ..VectorDBEnums import VectorDBEnums, QdrantEnums
import logging

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path:str, distance_metric:str):
        self.client=None
        self.db_path = db_path
        self.distance_metric = None

        if distance_metric.upper() == VectorDBEnums.COSINE.value:
            self.distance_metric = models.Distance.COSINE
        elif distance_metric.upper() == VectorDBEnums.DOT.value:
            self.distance_metric = models.Distance.DOT
        else:
            raise ValueError(f"Unsupported distance metric: {distance_metric}. Supported metrics are COSINE and DOT.")

        self.logger = logging.getLogger(__name__)
 

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_collections(self) -> list:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str):
         return self.client.get_collection(collection_name=collection_name)

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        if do_reset and self.is_collection_exists(collection_name):
            self.delete_collection(collection_name)
        if not self.is_collection_exists(collection_name):
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_metric)
            )
            return True
        else:
            self.logger.info(f"Collection {collection_name} already exists.")
            return False
        

    def delete_collection(self, collection_name: str):
        if self.is_collection_exists(collection_name):
            self.client.delete_collection(collection_name = collection_name)
            return True
        else:
            self.logger.info(f"Collection {collection_name} does not exist.")
            return False

    def insert_one(self, collection_name: str, text: str, vector: list, metadata: dict = None, record_id: str = None):
        if not self.is_collection_exists(collection_name):
            return False
        
        point = models.PointStruct(
            id=record_id,
            payload={"text": text, **(metadata or {})},
            vector=vector,
        )
        self.client.upsert(collection_name=collection_name, points=[point])
        return True

    def insert_many(self, collection_name: str, texts: list, vectors: list, metadatas: list = None, record_ids: list = None, batch_size: int = 100):
        if not self.is_collection_exists(collection_name):
            return False

        points = []
        for i in range(len(texts)):
            point = models.PointStruct(
                id=record_ids[i] if record_ids else None,
                payload={"text": texts[i], **(metadatas[i] if metadatas else {})},
                vector=vectors[i],
            )
            points.append(point)
            
            if len(points) >= batch_size:
                self.client.upload_points(
                    collection_name=collection_name,
                    records=points,  
                )
                points = []

        # Upload remaining points
        if points:
            self.client.upload_points(
                collection_name=collection_name,
                records=points,  # ✅ fixed from points= to records=
            )
        
        return True
    
    def search_by_vector(self,collection_name: str, query_vector: list, top_k: int):
        if not self.is_collection_exists(collection_name):
            return None

        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        return search_result