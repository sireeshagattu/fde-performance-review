from typing import Optional

import psycopg
from fastapi import APIRouter, FastAPI, HTTPException, Path, Query, Request
from models.Employee import Employee
from services.EmployeeService import list_employees
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.PerformanceReview import performance_review_create
import services.PerformanceReviewService as service
import services.ReviewPeriodService as review_period_service
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


@app.exception_handler(services.ReviewNotFoundError)
async def review_not_found_handler(request: Request, exc: services.ReviewNotFoundError):
    error = ErrorResponse(code="REVIEW_NOT_FOUND", message=str(exc))
    return JSONResponse(status_code=404, content=error.model_dump())


router = APIRouter(prefix="/api")


@router.get(
    "/reviews",
    response_model=list[Review],
    summary="List submitted performance reviews",
    description=(
        "Return reviews for the HR review register; optionally filter by the numeric employee primary key "
        "and review period primary key. An empty result is []."
    ),
    tags=["Mandatory - Reviews"],
    operation_id="listReviews",
    responses={503: {"model": ErrorResponse, "description": "Database is unavailable."}},
)
def list_reviews(
    employee_id: Optional[int] = Query(
        None, ge=1, description="employees.id (numeric DB key), not the EMP101-style code", examples=[1]
    ),
    period_id: Optional[int] = Query(None, ge=1, description="review_periods.id (numeric DB key)", examples=[1]),
):
    return services.list_reviews(employee_id=employee_id, period_id=period_id)

@app.get("/employees", response_model=list[Employee], tags=["Employees"])
def get_employees():
    try:
        return list_employees()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch employees"
        )

@router.get(
    "/reviews/{id}",
    response_model=Review,
    summary="Get one submitted review by ID",
    description="Optional classroom extension powering the read-only Review Details screen.",
    tags=["Optional - Review Details"],
    operation_id="getReviewById",
    responses={
        404: {"model": ErrorResponse, "description": "Review not found"},
        503: {"model": ErrorResponse, "description": "Database is unavailable."},
    },
)
def get_review(id: int = Path(..., ge=1, description="Numeric primary key of performance_reviews.id", examples=[101])):
    return services.get_review(id)


app.include_router(router)
@app.post("/performance-reviews")
def create_performance_review(payload: performance_review_create):
    service.save_performance_review(payload)
    return {"message": "Performance review created successfully"}

@app.get("/review-periods")
def get_review_periods():
    review_periods = review_period_service.get_all_review_periods_service()
    return {"review_periods": review_periods}