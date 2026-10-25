import repositories.ReviewPeriodRepository as reviewRepo

def create_review_period(review_period):
    reviewRepo.save_review(review_period)