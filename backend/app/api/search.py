from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.schemas.job import JobRead
from app.dependencies.database import get_db
from app.services.search_service import SearchService


router = APIRouter()


@router.get(
    "/jobs",
    response_model=list[JobRead],
)
def search_jobs(
    query: str | None = Query(default=None),
    category: str | None = Query(default=None),
    sub_category: str | None = Query(default=None),
    job_status: str | None = Query(default=None),
    application_mode: str | None = Query(default=None),
    is_featured: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return SearchService.search_jobs(
        db=db,
        query=query,
        category=category,
        sub_category=sub_category,
        job_status=job_status,
        application_mode=application_mode,
        is_featured=is_featured,
        page=page,
        limit=limit,
    )