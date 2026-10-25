from typing import Optional

import psycopg
from fastapi import APIRouter, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.ErrorResponse import ErrorResponse
from models.PerformanceReview import Review
from services import services

app = FastAPI(title="Employee Performance Review Management System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(psycopg.OperationalError)
async def database_unavailable_handler(request: Request, exc: psycopg.OperationalError):
    error = ErrorResponse(code="DATABASE_UNAVAILABLE", message="Database is unavailable. Try again later.")
    return JSONResponse(status_code=503, content=error.model_dump())


router = APIRouter(prefix="/api")


@router.get(
    "/reviews",
    response_model=list[Review],
    summary="List performance reviews",
    description="Returns performance reviews, newest first, optionally filtered by employee and/or review period.",
    tags=["Mandatory - Reviews"],
    operation_id="listReviews",
    responses={503: {"model": ErrorResponse, "description": "Database is unavailable."}},
)
def list_reviews(
    employee_id: Optional[int] = Query(None, ge=1, description="Only return reviews for this employee (internal ID)."),
    period_id: Optional[int] = Query(None, ge=1, description="Only return reviews for this review period."),
):
    return services.list_reviews(employee_id=employee_id, period_id=period_id)


app.include_router(router)
