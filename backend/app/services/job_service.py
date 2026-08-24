
from uuid import UUID


from sqlalchemy.orm import Session 
from sqlalchemy import or_


from app.database.models.job import Job






 
    
class JobService:

    @staticmethod
    def list_jobs(
        db: Session,
        search: str | None = None,
        category: str | None = None,
        job_status: str | None = None,
        is_featured: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ):
        query = db.query(Job)

        # Search
        if search:
            search_term = f"%{search}%"

            query = query.filter(
                or_(
                    Job.job_title.ilike(search_term),
                    Job.job_code.ilike(search_term),
                    Job.organization.ilike(search_term),
                )
            )

        # Category filter
        if category:
            query = query.filter(
                Job.category.ilike(category)
            )

        # Status filter
        if job_status:
            query = query.filter(
                Job.job_status.ilike(job_status)
            )

        # Featured filter
        if is_featured is not None:
            query = query.filter(
                Job.is_featured == is_featured
            )

        # Pagination
        offset = (page - 1) * limit

        return (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )
    @staticmethod
    def get_job(db:Session,job_id:UUID) -> Job| None:
        return (
            db.query(Job).filter(Job.id==job_id).first()
        )
        

    @staticmethod
    def create_job(db:Session,payload:dict) -> Job:
        job=Job(**payload)
        db.add(job)
        db.commit()
        db.refresh(job)
        
        return job

    
    
    @staticmethod
    def update_job(db: Session,job_id: UUID,payload: dict,) -> Job | None:

        job = (
        db.query(Job).filter(Job.id == job_id).first()
        )

        if  not job:
            return None

        for field, value in payload.items():
            setattr(job, field, value)

        db.commit()
        db.refresh(job)

        return job
    
    
    
    @staticmethod
    def delete_job(
        db: Session,
        job_id: UUID,
    ) -> bool:

        job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

        if not job:
            return False

        db.delete(job)
        db.commit()

        return True