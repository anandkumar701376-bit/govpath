from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models.job import Job
from app.database.models.mock_test import MockTest
from app.database.models.study import Roadmap
from app.database.models.study_task import StudyTask
from app.database.models.user import User


class AnalyticsService:
    @staticmethod
    def get_dashboard_summary(db: Session) -> dict[str, Any]:
        return {
            "total_users": db.query(User).count(),
            "active_users": db.query(User).filter(User.is_active.is_(True)).count(),
            "total_jobs": db.query(Job).count(),
            "featured_jobs": db.query(Job).filter(Job.is_featured.is_(True)).count(),
            "total_roadmaps": db.query(Roadmap).count(),
            "total_study_tasks": db.query(StudyTask).count(),
            "completed_study_tasks": db.query(StudyTask).filter(
                StudyTask.status.in_(["completed", "done", "finished"])
            ).count(),
            "total_mock_tests": db.query(MockTest).count(),
            "average_roadmap_completion": round(
                float(db.query(func.coalesce(func.avg(Roadmap.completion_percentage), 0.0)).scalar() or 0.0),
                2,
            ),
            "average_task_completion": round(
                float(db.query(func.coalesce(func.avg(StudyTask.completion_percentage), 0.0)).scalar() or 0.0),
                2,
            ),
        }
