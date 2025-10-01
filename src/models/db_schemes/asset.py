from datetime import datetime, timezone
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: ObjectId = Field(...)
    asset_name: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1)
    asset_size: Optional[int] = Field(default=None, gt=0)
    asset_config: Optional[Dict[str, Any]] = Field(default=None)
    asset_pushed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed= True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_indexes_1",
                "unique": False,
            },
            {
                "key": [("asset_project_id", 1), ("asset_name", 1)],
                "name": "asset_project_id_name_indexes_1",
                "unique": True,
            },
        ]


