from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath("."))

from backend.core.recommender import recommend_assessments

app = FastAPI(title="SHL Assessment Recommendation API")

DATA_PATH = "data/processed/shl_assessments.csv"

# -------- Load catalog ONCE --------
catalog_df = pd.read_csv(DATA_PATH)


# ---------- Schemas (PDF Appendix-2 compliant) ----------

class RecommendRequest(BaseModel):
    query: str
    k: int = 10


class AssessmentResponse(BaseModel):
    name: str
    url: str
    description: str
    duration: int
    remote_support: str
    adaptive_support: str
    test_type: List[str]


class RecommendResponse(BaseModel):
    recommendations: List[AssessmentResponse]


# ---------- Endpoints ----------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):

    results = recommend_assessments(
        query=req.query,
        df=catalog_df,
        k=req.k
    )

    response = []
    for r in results:
        response.append({
            "name": r.get("name", ""),
            "url": r.get("url", ""),
            "description": r.get("description", ""),
            "duration": int(r.get("duration", 0)),
            "remote_support": r.get("remote_support", "Yes"),
            "adaptive_support": r.get("adaptive_support", "No"),
            "test_type": r.get("test_type", [])
        })

    return {"recommendations": response}
