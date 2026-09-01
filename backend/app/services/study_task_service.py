from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.study_task import StudyTask


class StudyTaskService:

    @staticmethod
    def create(
        db: Session,
        data: dict,
    ) -> StudyTask:
        task = StudyTask(**data)

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def get_by_id(
        db: Session,
        task_id: UUID,
    ) -> StudyTask | None:
        return (
            db.query(StudyTask)
            .filter(StudyTask.id == task_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        user_id: UUID | None = None,
        job_id: UUID | None = None,
        roadmap_id: UUID | None = None,
        status: str | None = None,
    ) -> list[StudyTask]:

        query = db.query(StudyTask)

        if user_id is not None:
            query = query.filter(
                StudyTask.user_id == user_id
            )

        if job_id is not None:
            query = query.filter(
                StudyTask.job_id == job_id
            )

        if roadmap_id is not None:
            query = query.filter(
                StudyTask.roadmap_id == roadmap_id
            )

        if status is not None:
            query = query.filter(
                StudyTask.status == status
            )

        return (
            query
            .order_by(StudyTask.created_at.desc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        task: StudyTask,
        data: dict,
    ) -> StudyTask:

        for field, value in data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def delete(
        db: Session,
        task: StudyTask,
    ) -> None:

        db.delete(task)
        db.commit()