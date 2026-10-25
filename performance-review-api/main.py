from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.models.ReviewPeriod import review_periods as review_period
from app.repositories.ReviewPeriodRepository import save_review
import services as service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/review-periods")
def create_review_period(review_period: review_period):
    service.create_review_period(review_period)
    return {"message": "Review period created successfully"}

