from pydantic import BaseModel
from typing import List

class RecommendationDto(BaseModel):
    place_name: str
    expected_satisfaction: float
    sido: str
    sigungu: str

class RecommendationResponse(BaseModel):
    results: List[RecommendationDto]