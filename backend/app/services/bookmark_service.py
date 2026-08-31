from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models.bookmark import Bookmark


class BookmarkService:

    @staticmethod
    def create(
        db: Session,
        user_id: UUID,
        job_id: UUID,
    ) -> Bookmark:

        bookmark = Bookmark(
            user_id=user_id,
            job_id=job_id,
        )

        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)

        return bookmark

    @staticmethod
    def get_by_user_and_job(
        db: Session,
        user_id: UUID,
        job_id: UUID,
    ) -> Bookmark | None:

        return (
            db.query(Bookmark)
            .filter(
                Bookmark.user_id == user_id,
                Bookmark.job_id == job_id,
            )
            .first()
        )

    @staticmethod
    def list_by_user(
        db: Session,
        user_id: UUID,
    ) -> list[Bookmark]:

        return (
            db.query(Bookmark)
            .filter(Bookmark.user_id == user_id)
            .order_by(Bookmark.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        bookmark: Bookmark,
    ) -> None:

        db.delete(bookmark)
        db.commit()