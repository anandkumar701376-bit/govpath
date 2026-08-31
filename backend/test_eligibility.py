from datetime import date

from app.database.models.user_profile import UserProfile
from app.database.models.job_eligibility import JobEligibility
from app.services.eligibility_matching_service import (
    EligibilityMatchingService,
)


profile = UserProfile(
    date_of_birth=date(1990, 1, 1),
    education_level="graduation",
    degree="BSc",
    percentage=65,
    nationality="indian",
    experience_years=0,
)


eligibility = JobEligibility(
    minimum_age=18,
    maximum_age=30,
    age_relaxation_available=True,
    education_level="graduation",
    required_degree="BSc",
    minimum_percentage=60,
    nationality="indian",
    experience_required=False,
)


result = EligibilityMatchingService.check_eligibility(
    profile,
    eligibility,
)


print("ELIGIBILITY RESULT")
print("------------------")
print("Eligible:", result["eligible"])
print("Reasons:")

for reason in result["reasons"]:
    print("-", reason)