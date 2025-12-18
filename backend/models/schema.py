from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    query: str

class Assessment(BaseModel):
    name: str
    url: str
    description: str
    duration: int | None
    remote_support: str
    adaptive_support: str
    test_type: List[str]

class RecommendationResponse(BaseModel):
    recommended_assessments: List[Assessment]