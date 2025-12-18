from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import sys
import os

# allow backend imports
sys.path.append(os.path.abspath("."))

from backend.core.recommender import recommend_assessments

app = FastAPI(title="SHL Assessment Recommendation API")

DATA_PATH = "data/processed/shl_assessments.csv"


# ---------- Schemas (PDF Appendix-2 compliant) ----------

class RecommendRequest(BaseModel):
    query: str
    k: int = 10


class AssessmentResponse(BaseModel):
    name: str
    url: str


class RecommendResponse(BaseModel):
    recommendations: List[AssessmentResponse]


# ---------- Endpoints ----------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):

    df = pd.read_csv(DATA_PATH)

    results = recommend_assessments(
        query=req.query,
        df=df,
        k=req.k
    )

    response = [
        {"name": r["name"], "url": r["url"]}
        for r in results
    ]

    return {"recommendations": response}