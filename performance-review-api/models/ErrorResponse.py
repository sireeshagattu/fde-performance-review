from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Machine-readable error code.", examples=["DATABASE_UNAVAILABLE"])
    message: str = Field(
        ...,
        description="Human-readable error message.",
        examples=["Database is unavailable. Try again later."],
    )
