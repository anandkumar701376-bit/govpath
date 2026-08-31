from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.models.job import Job


class SearchService:

    @staticmethod
    def search_jobs(
        db: Session,
        query: str | None = None,
        category: str | None = None,
        sub_category: str | None = None,
        job_status: str | None = None,
        application_mode: str | None = None,
        is_featured: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> list[Job]:

        jobs_query = db.query(Job)

        # Keyword search
        if query:
            search_term = f"%{query}%"

            jobs_query = jobs_query.filter(
                or_(
                    Job.job_title.ilike(search_term),
                    Job.job_code.ilike(search_term),
                    Job.organization.ilike(search_term),
                    Job.description.ilike(search_term),
                )
            )

        # Category
        if category:
            jobs_query = jobs_query.filter(
                Job.category.ilike(category)
            )

        # Sub-category
        if sub_category:
            jobs_query = jobs_query.filter(
                Job.sub_category.ilike(sub_category)
            )

        # Status
        if job_status:
            jobs_query = jobs_query.filter(
                Job.job_status.ilike(job_status)
            )

        # Application mode
        if application_mode:
            jobs_query = jobs_query.filter(
                Job.application_mode.ilike(application_mode)
            )

        # Featured
        if is_featured is not None:
            jobs_query = jobs_query.filter(
                Job.is_featured == is_featured
            )

        # Pagination
        offset = (page - 1) * limit

        return (
            jobs_query
            .order_by(Job.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )