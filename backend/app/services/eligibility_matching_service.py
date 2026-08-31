from datetime import date
from decimal import Decimal

from app.database.models.job_eligibility import JobEligibility
from app.database.models.user_profile import UserProfile


class EligibilityMatchingService:

    @staticmethod
    def calculate_age(date_of_birth: date) -> int:
        today = date.today()

        age = today.year - date_of_birth.year

        if (today.month, today.day) < (
            date_of_birth.month,
            date_of_birth.day,
        ):
            age -= 1

        return age

    @staticmethod
    def check_eligibility(
        profile: UserProfile,
        eligibility: JobEligibility,
    ) -> dict:

        reasons = []
        eligible = True

        # -------------------------
        # Age
        # -------------------------

        if profile.date_of_birth is None:
            reasons.append("Date of birth is not provided.")
        else:
            age = EligibilityMatchingService.calculate_age(
                profile.date_of_birth
            )

            if eligibility.minimum_age is not None:
                if age < eligibility.minimum_age:
                    eligible = False
                    reasons.append(
                        f"Minimum age required is "
                        f"{eligibility.minimum_age}."
                    )

            if eligibility.maximum_age is not None:
                if age > eligibility.maximum_age:
                    if eligibility.age_relaxation_available:
                        reasons.append(
                            "Age exceeds the normal maximum age, "
                            "but age relaxation may be available."
                        )
                    else:
                        eligible = False
                        reasons.append(
                            f"Maximum age allowed is "
                            f"{eligibility.maximum_age}."
                        )

        # -------------------------
        # Education level
        # -------------------------

        if (
            eligibility.education_level
            and profile.education_level
        ):
            if (
                profile.education_level.strip().lower()
                != eligibility.education_level.strip().lower()
            ):
                eligible = False
                reasons.append(
                    f"Required education level is "
                    f"{eligibility.education_level}."
                )

        elif eligibility.education_level and not profile.education_level:
            reasons.append(
                "Education level is not provided."
            )

        # -------------------------
        # Degree
        # -------------------------

        if eligibility.required_degree:
            if not profile.degree:
                reasons.append(
                    "Required degree information is not provided."
                )
            elif (
                profile.degree.strip().lower()
                != eligibility.required_degree.strip().lower()
            ):
                eligible = False
                reasons.append(
                    f"Required degree is "
                    f"{eligibility.required_degree}."
                )

        # -------------------------
        # Percentage
        # -------------------------

        if eligibility.minimum_percentage is not None:
            if profile.percentage is None:
                reasons.append(
                    "Percentage is not provided."
                )
            elif (
                Decimal(str(profile.percentage))
                < Decimal(str(eligibility.minimum_percentage))
            ):
                eligible = False
                reasons.append(
                    f"Minimum percentage required is "
                    f"{eligibility.minimum_percentage}."
                )

        # -------------------------
        # Nationality
        # -------------------------

        if eligibility.nationality:
            if not profile.nationality:
                reasons.append(
                    "Nationality is not provided."
                )
            elif (
                profile.nationality.strip().lower()
                != eligibility.nationality.strip().lower()
            ):
                eligible = False
                reasons.append(
                    f"Required nationality is "
                    f"{eligibility.nationality}."
                )

        # -------------------------
        # Experience
        # -------------------------

        if eligibility.experience_required:
            if profile.experience_years is None:
                eligible = False
                reasons.append(
                    "Work experience information is not provided."
                )
            elif eligibility.minimum_experience_years is not None:
                if (
                    Decimal(str(profile.experience_years))
                    < Decimal(
                        str(
                            eligibility.minimum_experience_years
                        )
                    )
                ):
                    eligible = False
                    reasons.append(
                        f"Minimum experience required is "
                        f"{eligibility.minimum_experience_years} years."
                    )

        # -------------------------
        # Result
        # -------------------------

        if eligible:
            reasons.append(
                "User meets the available eligibility criteria."
            )

        return {
            "eligible": eligible,
            "reasons": reasons,
        }