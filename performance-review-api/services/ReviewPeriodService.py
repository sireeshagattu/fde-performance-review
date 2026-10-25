import repositories.ReviewPeriodRepository as repo

# write a function to get all review periods from repository.py and add validation to it
def get_all_review_periods_service() -> list:
    review_periods = repo.get_all_review_periods()
    if not review_periods:
        raise ValueError("No review periods found")
    return review_periods