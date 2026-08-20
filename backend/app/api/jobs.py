from fastapi import APIRouter, HTTPException, status

from app.database.schemas.job import JobCreate, JobRead
from app.services.job_service import JobService

router = APIRouter()


@router.get("/", response_model=list[JobRead])
def list_jobs():
    return [JobRead(**job) for job in JobService.list_jobs()]


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: str):
    job = JobService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobRead(**job)


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate):
    job = JobService.create_job(payload.model_dump())
    return JobRead(**job)
