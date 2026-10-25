
from pydantic import BaseModel
from datetime import date

class review_periods(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    status: str