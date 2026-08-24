from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.schemas.job_eligibility import (
    JobEligibilityCreate,
    JobEligibilityRead,
    JobEligibilityUpdate,
)
from app.dependencies.database import get_db
from app.services.job_eligibility_service import JobEligibilityService


router = APIRouter()


@router.post(
    "/jobs/{job_id}/eligibility",
    response_model=JobEligibilityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_job_eligibility(
    job_id: UUID,
    payload: JobEligibilityCreate,
    db: Session = Depends(get_db),
):
    existing = JobEligibilityService.get_by_job_id(db, job_id)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job eligibility already exists",
        )

    eligibility = JobEligibilityService.create(
        db,
        job_id,
        payload.model_dump(),
    )

    return eligibility


@router.get(
    "/jobs/{job_id}/eligibility",
    response_model=JobEligibilityRead,
)
def get_job_eligibility(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    eligibility = JobEligibilityService.get_by_job_id(
        db,
        job_id,
    )

    if not eligibility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job eligibility not found",
        )

    return eligibility


@router.patch(
    "/jobs/{job_id}/eligibility",
    response_model=JobEligibilityRead,
)
def update_job_eligibility(
    job_id: UUID,
    payload: JobEligibilityUpdate,
    db: Session = Depends(get_db),
):
    eligibility = JobEligibilityService.get_by_job_id(
        db,
        job_id,
    )

    if not eligibility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job eligibility not found",
        )

    updated = JobEligibilityService.update(
        db,
        eligibility,
        payload.model_dump(exclude_unset=True),
    )

    return updated


@router.delete(
    "/jobs/{job_id}/eligibility",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job_eligibility(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    eligibility = JobEligibilityService.get_by_job_id(
        db,
        job_id,
    )

    if not eligibility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job eligibility not found",
        )

    JobEligibilityService.delete(db, eligibility)

    return None