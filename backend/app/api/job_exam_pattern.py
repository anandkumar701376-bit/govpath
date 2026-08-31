from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.schemas.job_exam_pattern import (
    JobExamPatternCreate,
    JobExamPatternRead,
    JobExamPatternUpdate,
)
from app.dependencies.database import get_db
from app.services.job_exam_pattern_service import JobExamPatternService


router = APIRouter(
    tags=["Job Exam Pattern"]
)


@router.post(
    "/jobs/{job_id}/exam-pattern",
    response_model=JobExamPatternRead,
    status_code=status.HTTP_201_CREATED,
)
def create_exam_pattern(
    job_id: UUID,
    payload: JobExamPatternCreate,
    db: Session = Depends(get_db),
):
    exam_pattern = JobExamPatternService.create(
        db,
        job_id,
        payload.model_dump(),
    )

    return exam_pattern


@router.get(
    "/jobs/{job_id}/exam-pattern",
    response_model=list[JobExamPatternRead],
)
def get_exam_patterns(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    return JobExamPatternService.get_by_job_id(
        db,
        job_id,
    )


@router.get(
    "/exam-pattern/{exam_pattern_id}",
    response_model=JobExamPatternRead,
)
def get_exam_pattern(
    exam_pattern_id: UUID,
    db: Session = Depends(get_db),
):
    exam_pattern = JobExamPatternService.get_by_id(
        db,
        exam_pattern_id,
    )

    if not exam_pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam pattern not found",
        )

    return exam_pattern


@router.patch(
    "/exam-pattern/{exam_pattern_id}",
    response_model=JobExamPatternRead,
)
def update_exam_pattern(
    exam_pattern_id: UUID,
    payload: JobExamPatternUpdate,
    db: Session = Depends(get_db),
):
    exam_pattern = JobExamPatternService.get_by_id(
        db,
        exam_pattern_id,
    )

    if not exam_pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam pattern not found",
        )

    return JobExamPatternService.update(
        db,
        exam_pattern,
        payload.model_dump(exclude_unset=True),
    )


@router.delete(
    "/exam-pattern/{exam_pattern_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_exam_pattern(
    exam_pattern_id: UUID,
    db: Session = Depends(get_db),
):
    exam_pattern = JobExamPatternService.get_by_id(
        db,
        exam_pattern_id,
    )

    if not exam_pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam pattern not found",
        )

    JobExamPatternService.delete(
        db,
        exam_pattern,
    )

    return None