from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.schemas.study_task import (
    StudyTaskCreate,
    StudyTaskUpdate,
)
from app.services.study_task_service import StudyTaskService


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _as_uuid(value: str) -> UUID:
    try:
        return UUID(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format",
        ) from exc


def _task_response(task) -> Dict[str, Any]:
    return {
        "id": str(task.id),
        "roadmap_id": (
            str(task.roadmap_id)
            if task.roadmap_id else None
        ),
        "roadmap_stage_id": (
            str(task.roadmap_stage_id)
            if task.roadmap_stage_id else None
        ),
        "user_id": str(task.user_id),
        "job_id": (
            str(task.job_id)
            if task.job_id else None
        ),
        "task_title": task.task_title,
        "task_description": task.task_description,
        "task_type": task.task_type,
        "subject": task.subject,
        "topic": task.topic,
        "priority": task.priority,
        "estimated_duration_minutes": (
            task.estimated_duration_minutes
        ),
        "due_date": task.due_date,
        "status": task.status,
        "completion_percentage": (
            task.completion_percentage
        ),
        "ai_generated": task.ai_generated,
        "resource_id": (
            str(task.resource_id)
            if task.resource_id else None
        ),
        "notes": task.notes,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


@router.get("")
def list_study_tasks(
    user_id: Optional[str] = Query(default=None),
    job_id: Optional[str] = Query(default=None),
    roadmap_id: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:

    parsed_user_id = (
        _as_uuid(user_id)
        if user_id
        else None
    )

    parsed_job_id = (
        _as_uuid(job_id)
        if job_id
        else None
    )

    parsed_roadmap_id = (
        _as_uuid(roadmap_id)
        if roadmap_id
        else None
    )

    tasks = StudyTaskService.get_all(
        db,
        user_id=parsed_user_id,
        job_id=parsed_job_id,
        roadmap_id=parsed_roadmap_id,
        status=status,
    )

    return [
        _task_response(task)
        for task in tasks
    ]


@router.get("/{task_id}")
def get_study_task(
    task_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    task = StudyTaskService.get_by_id(
        db,
        _as_uuid(task_id),
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )

    return _task_response(task)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_study_task(
    payload: StudyTaskCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    task = StudyTaskService.create(
        db,
        payload.model_dump(),
    )

    return _task_response(task)


@router.patch("/{task_id}")
def update_study_task(
    task_id: str,
    payload: StudyTaskUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    task = StudyTaskService.get_by_id(
        db,
        _as_uuid(task_id),
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )

    task = StudyTaskService.update(
        db,
        task,
        payload.model_dump(exclude_unset=True),
    )

    return _task_response(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study_task(
    task_id: str,
    db: Session = Depends(get_db),
):
    task = StudyTaskService.get_by_id(
        db,
        _as_uuid(task_id),
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )

    StudyTaskService.delete(db, task)

    return None