from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.study import Subject


class SubjectService:

    @staticmethod
    def create(
        db: Session,
        data: dict,
    ) -> Subject:
        subject = Subject(
            **data,
        )

        db.add(subject)
        db.commit()
        db.refresh(subject)

        return subject

    @staticmethod
    def get_by_id(
        db: Session,
        subject_id: UUID,
    ) -> Subject | None:
        return (
            db.query(Subject)
            .filter(Subject.id == subject_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        active_only: bool | None = None,
    ) -> list[Subject]:
        query = db.query(Subject)

        if active_only is not None:
            query = query.filter(
                Subject.is_active == active_only
            )

        return (
            query
            .order_by(Subject.subject_name.asc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        subject: Subject,
        data: dict,
    ) -> Subject:
        for field, value in data.items():
            setattr(subject, field, value)

        db.commit()
        db.refresh(subject)

        return subject

    @staticmethod
    def delete(
        db: Session,
        subject: Subject,
    ) -> None:
        db.delete(subject)
        db.commit()