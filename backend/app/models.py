from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Movie(BaseModel):
    title: str
    title_en: Optional[str] = None
    year: int
    rating: float
    genres: List[str]
    description: str
    poster_url: Optional[str] = None
    reason: str


class RecommendRequest(BaseModel):
    prompt: str
    count: int = 3


class RecommendResponse(BaseModel):
    success: bool
    movies: List[Movie]
    query: str


class HistoryItem(BaseModel):
    id: int
    query: str
    movies: List[Movie]
    created_at: datetime
