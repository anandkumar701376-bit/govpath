from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.schemas.job_eligibility import (
    JobEligibilityCreate,
    JobEligibilityRead,
    JobEligibilityUpdate,
    EligibilityCheckRead,
)
from app.dependencies.database import get_db
from app.services.job_eligibility_service import JobEligibilityService

from app.database.models.user import User
from app.dependencies.auth import get_current_user
from app.services.eligibility_matching_service import(
    EligibilityMatchingService,
)


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

@router.get(
    "/jobs/{job_id}/eligibility/check",
    response_model=EligibilityCheckRead,
)
def check_job_eligibility(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = current_user.profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )

    eligibility = JobEligibilityService.get_by_job_id(
        db,
        job_id,
    )

    if not eligibility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job eligibility not found",
        )

    return EligibilityMatchingService.check_eligibility(
        profile,
        eligibility,
    )