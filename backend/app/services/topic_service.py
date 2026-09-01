from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.topic import Topic


class TopicService:

    @staticmethod
    def create(
        db: Session,
        data: dict,
    ) -> Topic:
        topic = Topic(**data)

        db.add(topic)
        db.commit()
        db.refresh(topic)

        return topic

    @staticmethod
    def get_by_id(
        db: Session,
        topic_id: UUID,
    ) -> Topic | None:
        return (
            db.query(Topic)
            .filter(Topic.id == topic_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        subject_id: UUID | None = None,
        active_only: bool | None = None,
    ) -> list[Topic]:
        query = db.query(Topic)

        if subject_id is not None:
            query = query.filter(
                Topic.subject_id == subject_id
            )

        if active_only is not None:
            query = query.filter(
                Topic.is_active == active_only
            )

        return (
            query
            .order_by(Topic.topic_name.asc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        topic: Topic,
        data: dict,
    ) -> Topic:
        for field, value in data.items():
            setattr(topic, field, value)

        db.commit()
        db.refresh(topic)

        return topic

    @staticmethod
    def delete(
        db: Session,
        topic: Topic,
    ) -> None:
        db.delete(topic)
        db.commit()