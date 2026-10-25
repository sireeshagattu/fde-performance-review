<<<<<<< HEAD
import repositories.ReviewPeriodRepository as repo

# write a function to get all review periods from repository.py and add validation to it
def get_all_review_periods_service() -> list:
    review_periods = repo.get_all_review_periods()
    if not review_periods:
        raise ValueError("No review periods found")
    return review_periods
=======
from repositories import ReviewPeriodRepository as rpRepo
from models.ReviewPeriod import review_periods
from models.ErrorResponse import ErrorResponse



def check_review_period_open(period_id: int): 
   review_period: review_periods = rpRepo.get_review_period(period_id)
   if review_period is None:
        error = ErrorResponse(code="REVIEW_PERIOD_NOT_FOUND", message="Review period not found")
        raise Exception(error.message)
   if not review_period.status.upper() == "open".upper():
        error = ErrorResponse(code="REVIEW_PERIOD_NOT_OPEN", message="The review period is not open for submissions")
        raise Exception(error.message)

def get_All_Review_Periods() -> list[review_periods]: 
    return rpRepo.get_all_review_periods()  
>>>>>>> feature/postreview
