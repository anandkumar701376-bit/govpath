from uuid import UUID


from fastapi import APIRouter,Depends,Query
from fastapi import  HTTPException, status
    
from sqlalchemy.orm import Session

from app.database.schemas.job import JobCreate, JobRead,JobUpdate
from app.dependencies.database import get_db
from app.services.job_service import JobService

from app.database.schemas.job import (
    JobCreate,JobRead,JobUpdate
)

router = APIRouter()


@router.get("/", response_model=list[JobRead])
def list_jobs(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    job_status: str | None = Query(default=None),
    is_featured: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return JobService.list_jobs(
        db=db,
        search=search,
        category=category,
        job_status=job_status,
        is_featured=is_featured,
        page=page,
        limit=limit,
    )
    
    
@router.get("/{job_id}", response_model=JobRead)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = JobService.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.post(
    "/",
    response_model=JobRead,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
):
    return JobService.create_job(
        db,
        payload.model_dump(),
    )
    
    
@router.patch(
    "/{job_id}",
    response_model=JobRead,
)
def update_job(
    job_id: UUID,
    payload: JobUpdate,
    db: Session = Depends(get_db),
):
    job = JobService.update_job(
        db,
        job_id,
        payload.model_dump(exclude_unset=True),
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = JobService.delete_job(db, job_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return {
        "message": "Job deleted successfully"
    }