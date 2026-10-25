import repositories.PerformanceReviewRepository as repo


def calculate_average_rating(quality: int, delivery: int, teamwork: int) -> float:
    return (quality + delivery + teamwork) / 3


def save_performance_review(payload):
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
