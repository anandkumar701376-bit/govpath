from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models.study import Roadmap, StudyTask, Subject, Topic
from app.database.schemas.study import SubjectCreate

from app.services.subject_service import SubjectService 


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format") from exc

@router.get("/subjects")
def list_subjects(
    active_only: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    subjects = SubjectService.get_all(
        db,
        active_only,
    )

    return [
        {
            "id": str(subject.id),
            "subject_name": subject.subject_name,
            "subject_code": subject.subject_code,
            "category": subject.category,
            "description": subject.description,
            "icon_url": subject.icon_url,
            "is_active": subject.is_active,
            "created_at": subject.created_at,
            "updated_at": subject.updated_at,
        }
        for subject in subjects
    ]


@router.get("/subjects/{subject_id}")
def get_subject(
    subject_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    subject = SubjectService.get_by_id(
        db,
        _as_uuid(subject_id),
    )

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return {
        "id": str(subject.id),
        "subject_name": subject.subject_name,
        "subject_code": subject.subject_code,
        "category": subject.category,
        "description": subject.description,
        "icon_url": subject.icon_url,
        "is_active": subject.is_active,
        "created_at": subject.created_at,
        "updated_at": subject.updated_at,
    }

@router.post(
    "/subjects",
    status_code=status.HTTP_201_CREATED,
)
def create_subject(
    payload: SubjectCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    subject = SubjectService.create(
        db,
        payload.model_dump(),
    )

    return {
        "id": str(subject.id),
        "subject_name": subject.subject_name,
        "subject_code": subject.subject_code,
        "category": subject.category,
        "description": subject.description,
        "icon_url": subject.icon_url,
        "is_active": subject.is_active,
        "created_at": subject.created_at,
        "updated_at": subject.updated_at,
    }