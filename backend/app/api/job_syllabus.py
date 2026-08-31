from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.schemas.job_syllabus import (
    JobSyllabusCreate,
    JobSyllabusRead,
    JobSyllabusUpdate,
)
from app.dependencies.database import get_db
from app.services.job_syllabus_service import JobSyllabusService


router = APIRouter(
    tags=["Job Syllabus"]
)

@router.post(
    "/jobs/{job_id}/syllabus",
    response_model=JobSyllabusRead,
    status_code=status.HTTP_201_CREATED,
)
def create_job_syllabus(
    job_id: UUID,
    payload: JobSyllabusCreate,
    db: Session = Depends(get_db),
):
    syllabus = JobSyllabusService.create(
        db,
        job_id,
        payload.model_dump(),
    )

    return syllabus


@router.get(
    "/jobs/{job_id}/syllabus",
    response_model=list[JobSyllabusRead],
)
def get_job_syllabus(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    return JobSyllabusService.get_by_job_id(
        db,
        job_id,
    )


@router.get(
    "/syllabus/{syllabus_id}",
    response_model=JobSyllabusRead,
)
def get_syllabus(
    syllabus_id: UUID,
    db: Session = Depends(get_db),
):
    syllabus = JobSyllabusService.get_by_id(
        db,
        syllabus_id,
    )

    if not syllabus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus not found",
        )

    return syllabus


@router.patch(
    "/syllabus/{syllabus_id}",
    response_model=JobSyllabusRead,
)
def update_syllabus(
    syllabus_id: UUID,
    payload: JobSyllabusUpdate,
    db: Session = Depends(get_db),
):
    syllabus = JobSyllabusService.get_by_id(
        db,
        syllabus_id,
    )

    if not syllabus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus not found",
        )

    return JobSyllabusService.update(
        db,
        syllabus,
        payload.model_dump(exclude_unset=True),
    )


@router.delete(
    "/syllabus/{syllabus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_syllabus(
    syllabus_id: UUID,
    db: Session = Depends(get_db),
):
    syllabus = JobSyllabusService.get_by_id(
        db,
        syllabus_id,
    )

    if not syllabus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus not found",
        )

    JobSyllabusService.delete(
        db,
        syllabus,
    )

    return None
