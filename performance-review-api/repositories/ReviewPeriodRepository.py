from app.db.database import get_connection
from app.models.ReviewPeriod import ReviewCreate


def save_review(review_period : ReviewCreate):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO review_periods (start_date, end_date) VALUES (%s, %s)",
        (review_period.start_date, review_period.end_date)
    )
    connection.commit()
    cursor.close()
    connection.close()

    