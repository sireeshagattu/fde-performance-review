from db.database import get_connection


def save_performance_review(
    employee_id: int,
    period_id: int,
    quality: int,
    delivery: int,
    teamwork: int,
    average_rating: float,
    comments: str = "",
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO performance_reviews (employee_id, period_id, quality_rating, delivery_rating, teamwork_rating, average_rating, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (employee_id, period_id, quality, delivery, teamwork, average_rating, comments),
            )
