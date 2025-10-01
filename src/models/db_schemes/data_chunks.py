from typing import Annotated, Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class DataChunks(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: Annotated[str, Field(min_length=1, description="Chunk content")]
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    chunk_order: Annotated[
        int, Field(gt=0, description="Order of the chunk in sequence")
    ]
    chunk_project_id: ObjectId

    class Config:
        arbitrary_types_allowed= True

    # Example validator: ensure chunk_text isn't just whitespace
    @field_validator("chunk_text")
    @classmethod
    def validate_chunk_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("chunk_text cannot be empty or whitespace")
        return value

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("chunk_project_id", 1)],
                "name": "chunk_project_id_indexes_1",
                "unique": False,
            }
        ]

