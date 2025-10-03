from enum import Enum

class VectorDBEnums(Enum):
    
    PINECONE = "PINECONE"
    WEAVIATE = "WEAVIATE"
    CHROMA = "CHROMA"
    VERTEX_AI = "VERTEX_AI"
    MILVUS = "MILVUS"
    QDRANT = "QDRANT"
    COSINE = 'COSINE'
    DOT = 'DOT'

class QdrantEnums(Enum):
    COLLECTION_NAME = "collection_name"
    VECTOR_NAME = "vector_name"
    VECTOR_DIMENSION = "vector_dimension"
    METADATA = "metadata"
    NAMESPACE = "namespace"
    DISTANCE = "distance"



class PineconeEnums(Enum):
    INDEX_NAME = "index_name"
    NAMESPACE = "namespace"
    METADATA = "metadata"

class WeaviateEnums(Enum):
    CLASS_NAME = "class_name"
    PROPERTIES = "properties"
    FILTER = "filter"
    NAMESPACE = "namespace"
    METADATA = "metadata"
    VECTOR_NAME = "vector_name"
    VECTOR_DIMENSION = "vector_dimension"
    VECTOR_INDEX_TYPE = "vector_index_type"
    VECTOR_METRIC = "vector_metric"
    VECTOR_EF_CONSTRUCTION = "vector_ef_construction"
    VECTOR_M = "vector_m"
    VECTOR_EF = "vector_ef"

class ChromaEnums(Enum):
    COLLECTION_NAME = "collection_name"
    METADATA = "metadata"
    NAMESPACE = "namespace"

class VertexAIEnums(Enum):
    INDEX_NAME = "index_name"
    METADATA = "metadata"   
    NAMESPACE = "namespace"

class MilvusEnums(Enum):
    COLLECTION_NAME = "collection_name"
    VECTOR_FIELD_NAME = "vector_field_name"
    VECTOR_DIMENSION = "vector_dimension"
    METADATA = "metadata"
    NAMESPACE = "namespace"
    INDEX_TYPE = "index_type"
    METRIC_TYPE = "metric_type"
    INDEX_PARAMS = "index_params"
