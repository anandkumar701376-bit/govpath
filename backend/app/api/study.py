from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models.study import Roadmap, StudyTask, Subject, Topic

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
    query = db.query(Subject)
    if active_only is not None:
        query = query.filter(Subject.is_active == active_only)

    subjects = query.order_by(Subject.subject_name.asc()).all()
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
def get_subject(subject_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    subject = db.query(Subject).filter(Subject.id == _as_uuid(subject_id)).first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
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


@router.post("/subjects", status_code=status.HTTP_201_CREATED)
def create_subject(payload: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    subject_name = (payload.get("subject_name") or "").strip()
    subject_code = (payload.get("subject_code") or "").strip()
    if not subject_name or not subject_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="subject_name and subject_code are required")

    subject = Subject(
        subject_name=subject_name,
        subject_code=subject_code,
        category=payload.get("category"),
        description=payload.get("description"),
        icon_url=payload.get("icon_url"),
        is_active=bool(payload.get("is_active", True)),
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
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


@router.get("/topics")
def list_topics(
    subject_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    query = db.query(Topic)
    if subject_id:
        query = query.filter(Topic.subject_id == _as_uuid(subject_id))

    topics = query.order_by(Topic.topic_name.asc()).all()
    return [
        {
            "id": str(topic.id),
            "subject_id": str(topic.subject_id),
            "topic_name": topic.topic_name,
            "topic_code": topic.topic_code,
            "difficulty_level": topic.difficulty_level,
            "weightage": float(topic.weightage) if topic.weightage is not None else None,
            "description": topic.description,
            "is_active": topic.is_active,
            "created_at": topic.created_at,
            "updated_at": topic.updated_at,
        }
        for topic in topics
    ]


@router.get("/topics/{topic_id}")
def get_topic(topic_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    topic = db.query(Topic).filter(Topic.id == _as_uuid(topic_id)).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return {
        "id": str(topic.id),
        "subject_id": str(topic.subject_id),
        "topic_name": topic.topic_name,
        "topic_code": topic.topic_code,
        "difficulty_level": topic.difficulty_level,
        "weightage": float(topic.weightage) if topic.weightage is not None else None,
        "description": topic.description,
        "is_active": topic.is_active,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
    }


@router.post("/topics", status_code=status.HTTP_201_CREATED)
def create_topic(payload: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    subject_id = payload.get("subject_id")
    topic_name = (payload.get("topic_name") or "").strip()
    if not subject_id or not topic_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="subject_id and topic_name are required")

    topic = Topic(
        subject_id=_as_uuid(subject_id),
        topic_name=topic_name,
        topic_code=payload.get("topic_code"),
        difficulty_level=payload.get("difficulty_level"),
        weightage=payload.get("weightage"),
        description=payload.get("description"),
        is_active=bool(payload.get("is_active", True)),
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return {
        "id": str(topic.id),
        "subject_id": str(topic.subject_id),
        "topic_name": topic.topic_name,
        "topic_code": topic.topic_code,
        "difficulty_level": topic.difficulty_level,
        "weightage": float(topic.weightage) if topic.weightage is not None else None,
        "description": topic.description,
        "is_active": topic.is_active,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at,
    }


@router.get("/roadmaps")
def list_roadmaps(
    user_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    query = db.query(Roadmap)
    if user_id:
        query = query.filter(Roadmap.user_id == _as_uuid(user_id))

    roadmaps = query.order_by(Roadmap.created_at.desc()).all()
    return [
        {
            "id": str(roadmap.id),
            "user_id": str(roadmap.user_id),
            "job_id": str(roadmap.job_id) if roadmap.job_id else None,
            "roadmap_title": roadmap.roadmap_title,
            "roadmap_type": roadmap.roadmap_type,
            "status": roadmap.status,
            "completion_percentage": float(roadmap.completion_percentage) if roadmap.completion_percentage is not None else None,
            "created_at": roadmap.created_at,
            "updated_at": roadmap.updated_at,
        }
        for roadmap in roadmaps
    ]


@router.get("/roadmaps/{roadmap_id}")
def get_roadmap(roadmap_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    roadmap = db.query(Roadmap).filter(Roadmap.id == _as_uuid(roadmap_id)).first()
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    return {
        "id": str(roadmap.id),
        "user_id": str(roadmap.user_id),
        "job_id": str(roadmap.job_id) if roadmap.job_id else None,
        "roadmap_title": roadmap.roadmap_title,
        "roadmap_type": roadmap.roadmap_type,
        "status": roadmap.status,
        "completion_percentage": float(roadmap.completion_percentage) if roadmap.completion_percentage is not None else None,
        "created_at": roadmap.created_at,
        "updated_at": roadmap.updated_at,
    }


@router.post("/roadmaps", status_code=status.HTTP_201_CREATED)
def create_roadmap(payload: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    user_id = payload.get("user_id")
    roadmap_title = (payload.get("roadmap_title") or "").strip()
    if not user_id or not roadmap_title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id and roadmap_title are required")

    roadmap = Roadmap(
        user_id=_as_uuid(user_id),
        job_id=_as_uuid(payload["job_id"]) if payload.get("job_id") else None,
        roadmap_title=roadmap_title,
        roadmap_type=payload.get("roadmap_type"),
        status=payload.get("status"),
        completion_percentage=payload.get("completion_percentage"),
        ai_generated=bool(payload.get("ai_generated", False)),
        notes=payload.get("notes"),
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    return {
        "id": str(roadmap.id),
        "user_id": str(roadmap.user_id),
        "job_id": str(roadmap.job_id) if roadmap.job_id else None,
        "roadmap_title": roadmap.roadmap_title,
        "roadmap_type": roadmap.roadmap_type,
        "status": roadmap.status,
        "completion_percentage": float(roadmap.completion_percentage) if roadmap.completion_percentage is not None else None,
        "created_at": roadmap.created_at,
        "updated_at": roadmap.updated_at,
    }


@router.get("/tasks")
def list_study_tasks(
    user_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    query = db.query(StudyTask)
    if user_id:
        query = query.filter(StudyTask.user_id == _as_uuid(user_id))

    tasks = query.order_by(StudyTask.created_at.desc()).all()
    return [
        {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "job_id": str(task.job_id) if task.job_id else None,
            "roadmap_id": str(task.roadmap_id) if task.roadmap_id else None,
            "task_title": task.task_title,
            "task_description": task.task_description,
            "task_type": task.task_type,
            "subject": task.subject,
            "topic": task.topic,
            "status": task.status,
            "completion_percentage": float(task.completion_percentage) if task.completion_percentage is not None else None,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }
        for task in tasks
    ]


@router.get("/tasks/{task_id}")
def get_study_task(task_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    task = db.query(StudyTask).filter(StudyTask.id == _as_uuid(task_id)).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study task not found")
    return {
        "id": str(task.id),
        "user_id": str(task.user_id),
        "job_id": str(task.job_id) if task.job_id else None,
        "roadmap_id": str(task.roadmap_id) if task.roadmap_id else None,
        "task_title": task.task_title,
        "task_description": task.task_description,
        "task_type": task.task_type,
        "subject": task.subject,
        "topic": task.topic,
        "status": task.status,
        "completion_percentage": float(task.completion_percentage) if task.completion_percentage is not None else None,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_study_task(payload: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    user_id = payload.get("user_id")
    task_title = (payload.get("task_title") or "").strip()
    if not user_id or not task_title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id and task_title are required")

    task = StudyTask(
        user_id=_as_uuid(user_id),
        roadmap_id=_as_uuid(payload["roadmap_id"]) if payload.get("roadmap_id") else None,
        job_id=_as_uuid(payload["job_id"]) if payload.get("job_id") else None,
        task_title=task_title,
        task_description=payload.get("task_description"),
        task_type=payload.get("task_type"),
        subject=payload.get("subject"),
        topic=payload.get("topic"),
        priority=payload.get("priority"),
        status=payload.get("status"),
        completion_percentage=payload.get("completion_percentage"),
        ai_generated=bool(payload.get("ai_generated", False)),
        notes=payload.get("notes"),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {
        "id": str(task.id),
        "user_id": str(task.user_id),
        "job_id": str(task.job_id) if task.job_id else None,
        "roadmap_id": str(task.roadmap_id) if task.roadmap_id else None,
        "task_title": task.task_title,
        "task_description": task.task_description,
        "task_type": task.task_type,
        "subject": task.subject,
        "topic": task.topic,
        "status": task.status,
        "completion_percentage": float(task.completion_percentage) if task.completion_percentage is not None else None,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }
