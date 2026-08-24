from uuid import UUID
from sqlalchemy.orm import Session

from app.database.models.job_eligibility import JobEligibility


class JobEligibilityService:

    @staticmethod
    def get_by_job_id(
        db: Session,
        job_id,
    ) -> JobEligibility | None:
        return (
            db.query(JobEligibility)
            .filter(JobEligibility.job_id == job_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        job_id,
        payload: dict,
    ) -> JobEligibility:

        eligibility = JobEligibility(
            job_id=job_id,
            **payload,
        )

        db.add(eligibility)
        db.commit()
        db.refresh(eligibility)

        return eligibility

    @staticmethod
    def update(
        db: Session,
        eligibility: JobEligibility,
        payload: dict,
    ) -> JobEligibility:

        for field, value in payload.items():
            setattr(eligibility, field, value)

        db.commit()
        db.refresh(eligibility)

        return eligibility

    @staticmethod
    def delete(
        db: Session,
        eligibility: JobEligibility,
    ) -> None:

        db.delete(eligibility)
        db.commit()