import repositories.PerformanceReviewRepository as prRepo
import services.ReviewPeriodService as rpService
from models.PerformanceReview import Review, ReviewStatus
from models.ErrorResponse import ErrorResponse


def validate_payload(payload):
    if not hasattr(payload, "employee_id") or payload.employee_id is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="employee_id is required")
        raise Exception(error.message)
    if not hasattr(payload, "period_id") or payload.period_id is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="period_id is required")
        raise Exception(error.message)
    if not hasattr(payload, "quality_rating") or payload.quality_rating is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="quality_rating is required")
        raise Exception(error.message)
    elif hasattr(payload, "quality_rating") and (payload.quality_rating < 1 or payload.quality_rating > 5):
        error = ErrorResponse(code="INVALID_PAYLOAD", message="quality_rating must be between 1 and 5")
        raise Exception(error.message)
    if not hasattr(payload, "delivery_rating") or payload.delivery_rating is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="delivery_rating is required")
        raise Exception(error.message)
    elif hasattr(payload, "delivery_rating") and (payload.delivery_rating < 1 or payload.delivery_rating > 5):
        error = ErrorResponse(code="INVALID_PAYLOAD", message="delivery_rating must be between 1 and 5")
        raise Exception(error.message)
    if not hasattr(payload, "teamwork_rating") or payload.teamwork_rating is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="teamwork_rating is required")
        raise Exception(error.message)
    elif hasattr(payload, "teamwork_rating") and (payload.teamwork_rating < 1 or payload.teamwork_rating > 5):
        error = ErrorResponse(code="INVALID_PAYLOAD", message="teamwork_rating must be between 1 and 5")
        raise Exception(error.message)
    if not hasattr(payload, "comments") or payload.comments is None:
        error = ErrorResponse(code="INVALID_PAYLOAD", message="comments is required")
        raise Exception(error.message)
    
#gururaj
class ReviewNotFoundError(Exception):
    def __init__(self, review_id):
        self.review_id = review_id
        super().__init__(f"No review exists with id {review_id}.")

class ReviewAlreadyExistsError(Exception):
    def __init__(self, employee_id, period_id):
        self.employee_id = employee_id
        self.period_id = period_id
        super().__init__("A review for this employee and period already exists")


#gururaj
def _to_review(row):
    return Review(**row, status=ReviewStatus.COMPLETED)

#gururaj
def list_reviews(employee_id=None, period_id=None):
    rows = prRepo.list_reviews(employee_id=employee_id, period_id=period_id)
    return [_to_review(row) for row in rows]

#gururaj
def get_review(review_id):
    row = prRepo.get_review(review_id)
    if row is None:
        raise ReviewNotFoundError(review_id)
    return _to_review(row)

def check_performance_review_exists(employee_id: int, period_id: int):
    existing_reviews = list_reviews(employee_id, period_id)
    if existing_reviews:
        raise ReviewAlreadyExistsError(employee_id, period_id)

   

def calculate_average_rating(quality: int, delivery: int, teamwork: int) -> float:
    return (quality + delivery + teamwork) / 3


def save_performance_review(payload):
    # Validate the payload before proceeding
    validate_payload(payload)

    # Check if a performance review for this employee and period already exists
    check_performance_review_exists(payload.employee_id, payload.period_id)

    #Check Review Period Open
    rpService.check_review_period_open(payload.period_id)

    # Calculate the average rating for the review
    average_rating = round(calculate_average_rating(
        payload.quality_rating, payload.delivery_rating, payload.teamwork_rating
    ))
    prRepo.save_performance_review(
        payload.employee_id,
        payload.period_id,
        payload.quality_rating,
        payload.delivery_rating,
        payload.teamwork_rating,
        average_rating,
        payload.comments,
    )
