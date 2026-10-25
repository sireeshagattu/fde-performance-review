from models.PerformanceReview import Review, ReviewStatus
from repositories import PerformanceReviewRepository


class ReviewNotFoundError(Exception):
    def __init__(self, review_id):
        self.review_id = review_id
        super().__init__(f"No review exists with id {review_id}.")


def _to_review(row):
    return Review(**row, status=ReviewStatus.COMPLETED)


def list_reviews(employee_id=None, period_id=None):
    rows = PerformanceReviewRepository.list_reviews(employee_id=employee_id, period_id=period_id)
    return [_to_review(row) for row in rows]


def get_review(review_id):
    row = PerformanceReviewRepository.get_review(review_id)
    if row is None:
        raise ReviewNotFoundError(review_id)
    return _to_review(row)
