from models.PerformanceReview import Review, ReviewStatus
from repositories import PerformanceReviewRepository


def list_reviews(employee_id=None, period_id=None):
    rows = PerformanceReviewRepository.list_reviews(employee_id=employee_id, period_id=period_id)
    return [Review(**row, status=ReviewStatus.COMPLETED) for row in rows]
