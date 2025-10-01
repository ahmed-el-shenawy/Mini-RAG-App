from typing import Optional

from pydantic import BaseModel


class ProcessRequest(BaseModel):
    asset_type: Optional[str] = None
    file_id: Optional[str] = None # ID of the file
    chunk_size: Optional[int] = 100  # Number of words per chunk
    overlap: Optional[int] = 20  # Number of overlapping words between chunks
    do_reset: Optional[int] = 0  # Whether to reset existing processed data
