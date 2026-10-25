from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer, field_validator


class ReviewStatus(str, Enum):
    COMPLETED = "Completed"


class Review(BaseModel):
    id: int = Field(..., ge=1, description="Unique identifier of the performance review.", examples=[101])
    employee_id: int = Field(..., ge=1, description="Internal ID of the reviewed employee.", examples=[1])
    employee_code: str = Field(
        ..., max_length=20, description="Business employee code of the reviewed employee.", examples=["EMP101"]
    )
    employee_name: str = Field(
        ..., max_length=100, description="Full name of the reviewed employee.", examples=["John Smith"]
    )
    period_id: int = Field(..., ge=1, description="ID of the review period.", examples=[1])
    period_name: str = Field(
        ..., max_length=50, description="Display name of the review period.", examples=["H2 2026 (Jul–Dec)"]
    )
    quality_rating: int = Field(..., ge=1, le=5, description="Quality of work rating (1-5).", examples=[4])
    delivery_rating: int = Field(..., ge=1, le=5, description="Delivery rating (1-5).", examples=[5])
    teamwork_rating: int = Field(..., ge=1, le=5, description="Teamwork rating (1-5).", examples=[4])
    average_rating: float = Field(
        ..., ge=1, le=5, description="Average of the three ratings, rounded to 2 decimals.", examples=[4.33]
    )
    comments: Optional[str] = Field(
        None,
        description="Reviewer comments.",
        examples=["Strong ownership and collaboration throughout the review period."],
    )
    status: ReviewStatus = Field(
        ReviewStatus.COMPLETED,
        description="Review status. Every stored review is Completed.",
        examples=[ReviewStatus.COMPLETED],
    )
    created_at: datetime = Field(
        ..., description="When the review was submitted (ISO 8601, UTC).", examples=["2026-10-25T09:30:00Z"]
    )

    @field_validator("average_rating", mode="before")
    @classmethod
    def _round_average(cls, value):
        # The database returns NUMERIC as Decimal; expose it as a 2-decimal JSON number.
        return round(float(value), 2)

    @field_serializer("created_at", when_used="json")
    def _serialize_created_at(self, value):
        # Naive database timestamps are stored in UTC.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
