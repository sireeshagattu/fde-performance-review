from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models.PerformanceReview import performance_review_create
import services.PerformanceReviewService as service


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/performance-reviews")
def create_performance_review(payload: performance_review_create):
    service.save_performance_review(payload)
    return {"message": "Performance review created successfully"}

