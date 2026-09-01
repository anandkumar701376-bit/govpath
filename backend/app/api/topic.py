from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.schemas.topic import (
    TopicCreate,
    TopicUpdate,
)
from app.services.topic_service import TopicService


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


@router.get("")
def list_topics(
    subject_id: Optional[str] = Query(default=None),
    active_only: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:

    parsed_subject_id = None

    if subject_id is not None:
        parsed_subject_id = _as_uuid(subject_id)

    topics = TopicService.get_all(
        db,
        subject_id=parsed_subject_id,
        active_only=active_only,
    )

    return [
        {
            "id": str(topic.id),
            "subject_id": str(topic.subject_id),
            "topic_name": topic.topic_name,
            "topic_code": topic.topic_code,
            "difficulty_level": topic.difficulty_level,
            "weightage": topic.weightage,
            "description": topic.description,
            "is_active": topic.is_active,
            "created_at": topic.created_at,
            "updated_at": topic.updated_at,
        }
        for topic in topics
    ]


@router.get("/{topic_id}")
def get_topic(
    topic_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    topic = TopicService.get_by_id(
        db,
        _as_uuid(topic_id),
    )

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    return {
        "id": str(topic.id),
        "subject_id": str(topic.subject_id),
        "topic_name": topic.topic_name,
        "topic_code": topic.topic_code,
        "difficulty_level": topic.difficulty_level,
        "weightage": topic.weightage,
        "description": topic.description,
        "is_active": topic.is_active,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
    }


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    payload: TopicCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    topic = TopicService.create(
        db,
        payload.model_dump(),
    )

    return {
        "id": str(topic.id),
        "subject_id": str(topic.subject_id),
        "topic_name": topic.topic_name,
        "topic_code": topic.topic_code,
        "difficulty_level": topic.difficulty_level,
        "weightage": topic.weightage,
        "description": topic.description,
        "is_active": topic.is_active,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
    }


@router.patch("/{topic_id}")
def update_topic(
    topic_id: str,
    payload: TopicUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:

    topic = TopicService.get_by_id(
        db,
        _as_uuid(topic_id),
    )

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    topic = TopicService.update(
        db,
        topic,
        payload.model_dump(exclude_unset=True),
    )

    return {
        "id": str(topic.id),
        "subject_id": str(topic.subject_id),
        "topic_name": topic.topic_name,
        "topic_code": topic.topic_code,
        "difficulty_level": topic.difficulty_level,
        "weightage": topic.weightage,
        "description": topic.description,
        "is_active": topic.is_active,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
    }


@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_topic(
    topic_id: str,
    db: Session = Depends(get_db),
):
    topic = TopicService.get_by_id(
        db,
        _as_uuid(topic_id),
    )

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    TopicService.delete(db, topic)

    return None