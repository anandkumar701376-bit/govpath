from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models.job import Job
from app.database.models.mock_test import MockTest
from app.database.models.study import Roadmap, StudyTask
from app.database.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/overview")
def analytics_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    active_users = db.query(User).filter(User.is_active.is_(True)).count()
    featured_jobs = db.query(Job).filter(Job.is_featured.is_(True)).count()
    avg_roadmap_completion = db.query(
        func.coalesce(func.avg(Roadmap.completion_percentage), 0.0)
    ).scalar() or 0.0
    avg_task_completion = db.query(
        func.coalesce(func.avg(StudyTask.completion_percentage), 0.0)
    ).scalar() or 0.0
    completed_tasks = db.query(StudyTask).filter(
        StudyTask.status.in_(["completed", "done", "finished"])
    ).count()

    return {
        "total_users": db.query(User).count(),
        "active_users": active_users,
        "total_jobs": db.query(Job).count(),
        "featured_jobs": featured_jobs,
        "total_roadmaps": db.query(Roadmap).count(),
        "total_study_tasks": db.query(StudyTask).count(),
        "completed_study_tasks": completed_tasks,
        "total_mock_tests": db.query(MockTest).count(),
        "average_roadmap_completion": round(float(avg_roadmap_completion), 2),
        "average_task_completion": round(float(avg_task_completion), 2),
    }


@router.get("/users")
def analytics_users(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    users = db.query(User).order_by(User.created_at.desc()).all()
    data: List[Dict[str, Any]] = []

    for user in users:
        roadmap_count = db.query(Roadmap).filter(Roadmap.user_id == user.id).count()
        task_count = db.query(StudyTask).filter(StudyTask.user_id == user.id).count()
        completed_tasks = db.query(StudyTask).filter(
            StudyTask.user_id == user.id,
            StudyTask.status.in_(["completed", "done", "finished"]),
        ).count()
        avg_task_completion = db.query(
            func.coalesce(func.avg(StudyTask.completion_percentage), 0.0)
        ).filter(StudyTask.user_id == user.id).scalar() or 0.0

        data.append(
            {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "last_login": user.last_login,
                "roadmap_count": roadmap_count,
                "task_count": task_count,
                "completed_tasks": completed_tasks,
                "average_task_completion": round(float(avg_task_completion), 2),
            }
        )

    return data


@router.get("/jobs")
def analytics_jobs(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    data: List[Dict[str, Any]] = []

    for job in jobs:
        roadmap_count = db.query(Roadmap).filter(Roadmap.job_id == job.id).count()
        task_count = db.query(StudyTask).filter(StudyTask.job_id == job.id).count()
        avg_roadmap_completion = db.query(
            func.coalesce(func.avg(Roadmap.completion_percentage), 0.0)
        ).filter(Roadmap.job_id == job.id).scalar() or 0.0

        data.append(
            {
                "id": str(job.id),
                "job_title": job.job_title,
                "job_code": job.job_code,
                "organization": job.organization,
                "category": job.category,
                "is_featured": job.is_featured,
                "job_status": job.job_status,
                "roadmap_count": roadmap_count,
                "task_count": task_count,
                "average_roadmap_completion": round(float(avg_roadmap_completion), 2),
            }
        )

    return data
