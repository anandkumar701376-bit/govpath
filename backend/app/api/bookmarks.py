from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.models.bookmark import Bookmark
from app.database.models.job import Job
from app.database.models.user import User
from app.database.schemas.bookmark import BookmarkRead
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.services.bookmark_service import BookmarkService


router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


@router.post(
    "/jobs/{job_id}",
    response_model=BookmarkRead,
    status_code=status.HTTP_201_CREATED,
)
def create_bookmark(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    existing = BookmarkService.get_by_user_and_job(
        db,
        current_user.id,
        job_id,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job already bookmarked",
        )

    return BookmarkService.create(
        db,
        current_user.id,
        job_id,
    )


@router.get(
    "/",
    response_model=list[BookmarkRead],
)
def list_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return BookmarkService.list_by_user(
        db,
        current_user.id,
    )


@router.delete(
    "/jobs/{job_id}",
)
def delete_bookmark(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bookmark = BookmarkService.get_by_user_and_job(
        db,
        current_user.id,
        job_id,
    )

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    BookmarkService.delete(db, bookmark)

    return {
        "message": "Bookmark removed successfully"
    }