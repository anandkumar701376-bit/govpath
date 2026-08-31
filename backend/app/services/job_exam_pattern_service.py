from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.job_exam_pattern import JobExamPattern


class JobExamPatternService:

    @staticmethod
    def create(
        db: Session,
        job_id: UUID,
        data: dict,
    ) -> JobExamPattern:
        exam_pattern = JobExamPattern(
            job_id=job_id,
            **data,
        )

        db.add(exam_pattern)
        db.commit()
        db.refresh(exam_pattern)

        return exam_pattern

    @staticmethod
    def get_by_id(
        db: Session,
        exam_pattern_id: UUID,
    ) -> JobExamPattern | None:
        return (
            db.query(JobExamPattern)
            .filter(JobExamPattern.id == exam_pattern_id)
            .first()
        )

    @staticmethod
    def get_by_job_id(
        db: Session,
        job_id: UUID,
    ) -> list[JobExamPattern]:
        return (
            db.query(JobExamPattern)
            .filter(JobExamPattern.job_id == job_id)
            .order_by(JobExamPattern.stage_order)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        exam_pattern: JobExamPattern,
        data: dict,
    ) -> JobExamPattern:
        for field, value in data.items():
            setattr(exam_pattern, field, value)

        db.commit()
        db.refresh(exam_pattern)

        return exam_pattern

    @staticmethod
    def delete(
        db: Session,
        exam_pattern: JobExamPattern,
    ) -> None:
        db.delete(exam_pattern)
        db.commit()