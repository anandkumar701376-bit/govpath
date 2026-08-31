from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.job_syllabus import JobSyllabus


class JobSyllabusService:

    @staticmethod
    def create(
        db: Session,
        job_id: UUID,
        data: dict,
    ) -> JobSyllabus:
        syllabus = JobSyllabus(
            job_id=job_id,
            **data,
        )

        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)

        return syllabus

    @staticmethod
    def get_by_id(
        db: Session,
        syllabus_id: UUID,
    ) -> JobSyllabus | None:
        return (
            db.query(JobSyllabus)
            .filter(JobSyllabus.id == syllabus_id)
            .first()
        )

    @staticmethod
    def get_by_job_id(
        db: Session,
        job_id: UUID,
    ) -> list[JobSyllabus]:
        return (
            db.query(JobSyllabus)
            .filter(JobSyllabus.job_id == job_id)
            .order_by(
                JobSyllabus.stage_name,
                JobSyllabus.subject_name,
                JobSyllabus.topic_name,
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        syllabus: JobSyllabus,
        data: dict,
    ) -> JobSyllabus:
        for field, value in data.items():
            setattr(syllabus, field, value)

        db.commit()
        db.refresh(syllabus)

        return syllabus

    @staticmethod
    def delete(
        db: Session,
        syllabus: JobSyllabus,
    ) -> None:
        db.delete(syllabus)
        db.commit()