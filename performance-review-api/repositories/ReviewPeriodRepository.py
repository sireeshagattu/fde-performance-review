from db.database import get_connection
# from table review_periods create a function to get all review periods from the database
def get_all_review_periods():
    connection = get_connection()
    if connection is None:
        raise RuntimeError("Database connection could not be established.")
    cursor = connection.cursor()
    # if review_periods table does not exist, throw Error
    try:
        cursor.execute("SELECT * FROM review_periods")
    except Exception as e:
        raise RuntimeError(f"Error fetching review periods: {e}") from e
    review_periods = cursor.fetchall()
    cursor.close()
    connection.close()
    print("data "+str(review_periods))
    return review_periods