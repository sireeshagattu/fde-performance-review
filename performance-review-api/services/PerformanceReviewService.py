import repositories.PerformanceReviewRepository as repo

def validate_payload(payload):
    if not hasattr(payload, "employee_id") or payload.employee_id is None:
        raise ValueError("employee_id is required")
    if not hasattr(payload, "period_id") or payload.period_id is None:
        raise ValueError("period_id is required")
    if not hasattr(payload, "quality_rating") or payload.quality_rating is None:
        raise ValueError("quality_rating is required")
    elif hasattr(payload, "quality_rating") and (payload.quality_rating < 1 or payload.quality_rating > 5):
        raise ValueError("quality_rating must be between 1 and 5")
    if not hasattr(payload, "delivery_rating") or payload.delivery_rating is None:
        raise ValueError("delivery_rating is required")
    elif hasattr(payload, "delivery_rating") and (payload.delivery_rating < 1 or payload.delivery_rating > 5):
        raise ValueError("delivery_rating must be between 1 and 5")
    if not hasattr(payload, "teamwork_rating") or payload.teamwork_rating is None:
        raise ValueError("teamwork_rating is required")
    elif hasattr(payload, "teamwork_rating") and (payload.teamwork_rating < 1 or payload.teamwork_rating > 5):
        raise ValueError("teamwork_rating must be between 1 and 5")
    if not hasattr(payload, "comments") or payload.comments is None:
        raise ValueError("comments is required")


def calculate_average_rating(quality: int, delivery: int, teamwork: int) -> float:
    return (quality + delivery + teamwork) / 3


def save_performance_review(payload):
    validate_payload(payload)
    average_rating = calculate_average_rating(
        payload.quality_rating, payload.delivery_rating, payload.teamwork_rating
    )
    repo.save_performance_review(
        payload.employee_id,
        payload.period_id,
        payload.quality_rating,
        payload.delivery_rating,
        payload.teamwork_rating,
        average_rating,
        payload.comments,
    )
