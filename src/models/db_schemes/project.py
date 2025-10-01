from typing import Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    """Project model for MongoDB integration."""

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: Annotated[
        str, Field(min_length=1, description="Unique project identifier")
    ]

    class Config:
        arbitrary_types_allowed= True

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        """Validate that project_id is alphanumeric."""
        if not value.isalnum():
            raise ValueError("The project_id must be alphanumeric")
        return value

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("project_id", 1)],
                "name": "project_id_indexes_1",
                "unique": True,
            },
        ]

