from typing import List, Optional
from pydantic import BaseModel


class SearchResult(BaseModel):
    job_id: int
    title: str
    category: str
    similarity_score: float

class PaginatedResponse(BaseModel):
    results: List[SearchResult]
    next_page_offset: Optional[str]
    total_count: int

