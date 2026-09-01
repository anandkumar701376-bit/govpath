from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models.job import Job
from app.database.models.mock_test import MockTest
from app.database.models.topic import Topic
from app.database.models.study import Roadmap,  Subject
from app.database.models.study_task import StudyTask
from app.database.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/overview')
def admin_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    summary = {
        'total_users': db.query(User).count(),
        'total_jobs': db.query(Job).count(),
        'total_subjects': db.query(Subject).count(),
        'total_topics': db.query(Topic).count(),
        'total_roadmaps': db.query(Roadmap).count(),
        'total_study_tasks': db.query(StudyTask).count(),
        'total_mock_tests': db.query(MockTest).count(),
    }
    return summary


@router.get('/users')
def list_users(
    active_only: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if active_only is not None:
        query = query.filter(User.is_active == active_only)
    users = query.order_by(User.created_at.desc()).all()
    return [
        {
            'id': str(user.id),
            'full_name': user.full_name,
            'email': user.email,
            'mobile_number': user.mobile_number,
            'is_active': user.is_active,
            'role': user.role,
            'last_login': user.last_login,
            'created_at': user.created_at,
        }
        for user in users
    ]


@router.get('/jobs')
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return [
        {
            'id': str(job.id),
            'job_title': job.job_title,
            'job_code': job.job_code,
            'organization': job.organization,
            'category': job.category,
            'job_status': job.job_status,
            'is_featured': job.is_featured,
            'application_start_date': job.application_start_date,
            'application_end_date': job.application_end_date,
            'created_at': job.created_at,
        }
        for job in jobs
    ]


@router.get('/subjects')
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).order_by(Subject.subject_name.asc()).all()
    return [
        {
            'id': str(subject.id),
            'subject_name': subject.subject_name,
            'subject_code': subject.subject_code,
            'category': subject.category,
            'is_active': subject.is_active,
            'created_at': subject.created_at,
        }
        for subject in subjects
    ]


@router.get('/roadmaps')
def list_roadmaps(db: Session = Depends(get_db)):
    roadmaps = db.query(Roadmap).order_by(Roadmap.created_at.desc()).all()
    return [
        {
            'id': str(roadmap.id),
            'user_id': str(roadmap.user_id),
            'job_id': str(roadmap.job_id) if roadmap.job_id else None,
            'roadmap_title': roadmap.roadmap_title,
            'status': roadmap.status,
            'completion_percentage': roadmap.completion_percentage,
            'created_at': roadmap.created_at,
        }
        for roadmap in roadmaps
    ]


@router.put('/users/{user_id}/toggle-active', status_code=status.HTTP_200_OK)
def toggle_user_active(user_id: str, is_active: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user.is_active = is_active
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return {'id': str(user.id), 'is_active': user.is_active}


@router.put('/jobs/{job_id}/toggle-featured', status_code=status.HTTP_200_OK)
def toggle_job_featured(job_id: str, is_featured: bool, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')

    job.is_featured = is_featured
    job.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(job)
    return {'id': str(job.id), 'is_featured': job.is_featured}
