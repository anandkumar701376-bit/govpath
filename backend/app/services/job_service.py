from datetime import datetime
from typing import Any


from sqlalchemy.orm import Session 
from app.database.models.job import Job

from  sqlalchemy.dialects.postgresql import UUID


class JobService:
    @staticmethod
    def list_jobs(db:Session) -> list[Job]:
        return db.query(Job).all()

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
